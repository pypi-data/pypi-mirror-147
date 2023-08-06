"""Topological Neural Network classes"""
import abc

import numpy as np
import pandas
import plotly.express as px
import plotly.graph_objects as go
import torch
from plotly.subplots import make_subplots
from sklearn.datasets import make_blobs
from torch import nn, optim
from torch.optim.lr_scheduler import LambdaLR

from persistent_homology import FilteredComplexes, MatrixReduction


class AbstractAutoencoder(nn.Module, metaclass=abc.ABCMeta):
    """Abstract base class for our Autoencoders. Including methods: forward, encode_into_latent_space, decode_from_latent_space"""

    @abc.abstractmethod
    def forward(self, x):
        """Forward function for the for neural network model."""

    @abc.abstractmethod
    def encode_into_latent_space(self, x):
        """Calculates the coding in latent space."""

    @abc.abstractmethod
    def decode_from_latent_space(self, z):
        """Inverse operation to "encode_into_latent_space()"."""


class FullyConnectedAutoencoder(AbstractAutoencoder):
    """Fully connected network with latent space which has 2 dimensions and takes in 3-dimensional data."""

    def __init__(self, encoder=None, decoder=None, loss=None):
        super().__init__()
        if encoder:
            self.encoder = encoder
        else:
            self.encoder = torch.nn.Sequential(
                nn.Linear(in_features=3, out_features=512),
                nn.ReLU(),
                nn.Linear(in_features=512, out_features=256),
                nn.ReLU(),
                nn.Linear(in_features=256, out_features=128),
                nn.ReLU(),
                nn.Linear(in_features=128, out_features=64),
                nn.ReLU(),
                nn.Linear(in_features=64, out_features=2),
            )
        if decoder:
            self.decoder = decoder
        else:
            self.decoder = torch.nn.Sequential(
                nn.Linear(in_features=2, out_features=64),
                nn.ReLU(),
                nn.Linear(in_features=64, out_features=128),
                nn.ReLU(),
                nn.Linear(in_features=128, out_features=256),
                nn.ReLU(),
                nn.Linear(in_features=256, out_features=512),
                nn.ReLU(),
                nn.Linear(in_features=512, out_features=3),
                torch.nn.Sigmoid()
            )
        if loss:
            self.reconstruction_error = loss
        else:
            self.reconstruction_error = nn.MSELoss()

    def encode_into_latent_space(self, x):
        """Computes the latent representation using our autoencoder.
        :param x: input data in space X
        :type x: torch.Tensor
        :return: output data in space Z
        :rtype: torch.Tensor
        """
        x = self.encoder(x)
        return x

    def decode_from_latent_space(self, z):
        """Compute the reconstruction using our autoencoder.
        :param z: Input data in space Z
        :type z: torch.Tensor
        :return: Output data in space X
        :rtype: torch.Tensor
        """
        z = self.decoder(z)
        return z

    def forward(self, original_data):
        """Applies our autoencoder to a batch of data.
        :param original_data: Input data in space X
        :type original_data: torch.Tensor
        :return: Reconstruction error of X and decode(encode(x)) as MSELoss.
        :rtype: torch.Tensor
        """
        data_latent = self.encode_into_latent_space(original_data)
        data_reconstructed = self.decode_from_latent_space(data_latent)
        print(original_data.size())
        print(data_reconstructed.size())
        reconstruction_error = self.reconstruction_error(original_data, data_reconstructed)
        print(f"Reconstruction Error: {reconstruction_error:.5f}")
        return reconstruction_error


class ConvolutionalAutoencoder(AbstractAutoencoder):
    """Convolutional network with latent space which has 2 dimensions."""

    def __init__(self, encoder=None, decoder=None, loss=None):
        """Convolutional Autoencoder."""
        super().__init__()
        if encoder:
            self.encoder = encoder
        else:
            self.encoder = torch.nn.Sequential(
                nn.Conv2d(in_channels=3, out_channels=12, kernel_size=3),
                nn.ReLU(),
                nn.Conv2d(in_channels=12, out_channels=24, kernel_size=5),
                nn.ReLU(),
                nn.Conv2d(in_channels=24, out_channels=48, kernel_size=3),
                nn.ReLU(),
            )
        if decoder:
            self.decoder = decoder
        else:
            self.decoder = torch.nn.Sequential(
                nn.ConvTranspose2d(in_channels=48, out_channels=24, kernel_size=3),
                nn.ReLU(),
                nn.ConvTranspose2d(in_channels=24, out_channels=12, kernel_size=5),
                nn.ReLU(),
                nn.ConvTranspose2d(in_channels=12, out_channels=3, kernel_size=3),
                # Sigmoid function to get all between 0 and 2 again
                nn.Sigmoid(),
            )
        if loss:
            self.reconstruction_error = loss
        else:
            self.reconstruction_error = nn.MSELoss()

    def encode_into_latent_space(self, x):
        """Computes the latent representation using our autoencoder.
        :param x: input data in space X
        :type x: torch.Tensor
        :return: output data in space Z
        :rtype: torch.Tensor
        """
        x = self.encoder(x)
        return x

    def decode_from_latent_space(self, z):
        """Compute the reconstruction using our autoencoder.
        :param z: Input data in space Z
        :type z: torch.Tensor
        :return: Output data in space X
        :rtype: torch.Tensor
        """
        z = self.decoder(z)
        return z

    def forward(self, original_data):
        """Applies our autoencoder to a batch of data.
        :param original_data: Input data in space X
        :type original_data: torch.Tensor
        :return: Reconstruction error of X and decode(encode(x)) as MSELoss.
        :rtype: torch.Tensor
        """
        data_latent = self.encode_into_latent_space(original_data)
        data_reconstructed = self.decode_from_latent_space(data_latent)
        fig = px.scatter(original_data)
        fig.show()
        px.scatter(data_latent)
        print(original_data.size())
        print(data_reconstructed.size())
        reconstruction_error = self.reconstruction_error(original_data, data_reconstructed)
        print(f"Reconstruction Error: {reconstruction_error:.5f}")
        return reconstruction_error


class TopologicalAutoencoder(nn.Module):
    """Topologically regularized autoencoder."""

    def __init__(self, autoencoder_model='FullyConnectedAutoencoder', regularization_lambda=0.3):
        """Topological Autoencoder
        :param autoencoder_model: Decides which kind of model is actually used
        :type autoencoder_model: str
        :param regularization_lambda: Regularization strength of the topology part
        :type regularization_lambda: float
        """
        super().__init__()
        self.regularization_lambda = regularization_lambda
        if autoencoder_model == "ConvolutionalAutoencoder":
            self.autoencoder = ConvolutionalAutoencoder()
        if autoencoder_model == "FullyConnectedAutoencoder":
            self.autoencoder = FullyConnectedAutoencoder()
        else:
            raise NotImplementedError

    def _calculate_tensor_distance_matrix(self, x):
        """Calculates internally the distance matrix for the input vector.
        :param x: Input tensor
        :type x: torch.Tensor
        :return: Matrix with euclidean distances in tensor form
        :rtype: torch.Tensor
        """
        x_flatten = x.view(x.size(0), -1)  # We flatten down to (batch_size, rest)
        distances = torch.cdist(x_flatten, x_flatten, p=2)  # dimension should be (batch_size,batch_size)
        return distances

    def _calculate_topological_distance(self, data_x, data_z):
        """Return topological distance of two tensor distance matrices.
        :param data_x: input tensor in the space X
        :type data_x: torch.Tensor
        :param data_z: input tensor in the sapce Z
        :type data_z: torch.Tensor
        :return: The topological distance as loss
        :rtype: float
        """

        # calculate the persistent homology for the batch in X and in Z based on the distances.
        # We wrote a new function for that, since we start from the distance matrices and not from
        pairs = dict()
        barcodes = dict()
        distances = dict()
        distance_lists = dict()
        simplices = dict()
        # Get the reduced boundary matrices by calculating the complexes for the data in data space X and latent space Z
        for idx, data in enumerate([data_x, data_z]):
            dist_matrix = self._calculate_tensor_distance_matrix(data)
            distances[idx] = dist_matrix.detach().cpu().numpy()
            filtered_complex = FilteredComplexes()
            boundary_matrix, dimensions_array, distance_list = filtered_complex.fit(
                own_dist_matrix=dist_matrix.detach().cpu().numpy(),
                max_simplices_dim=3)  # We will never go over dimension 3 with a batch size of 4
            matrix_reductor = MatrixReduction(boundary_matrix=boundary_matrix, distance_list=distance_list,
                                              boundary_matrix_dimens=dimensions_array)
            matrix_reductor.reduce_boundary_matrix()
            distance_lists[idx] = np.array(distance_list)
            simplices[idx] = filtered_complex.get_simplices()
            pairs[idx] = matrix_reductor.get_persistence_pairs()
            pairs[idx] = pairs[idx][np.inf != pairs[idx]["death"]]
            barcodes[idx] = matrix_reductor.get_barcode_of_reduced_matrix()
            barcodes[idx] = barcodes[idx][np.inf != barcodes[idx]["death_value"]]

        # --- getting relevant edges ---
        complex_x = simplices[0]
        # We sort out the points on the diagonal on the persistence diagrams
        dying_simplicies_index_x = complex_x.loc[complex_x["edge_death_index"] != -1, "index"]
        dying_simplicies_index_minus_one_x = dying_simplicies_index_x - 1
        complex_x = complex_x[~complex_x["index"].isin(dying_simplicies_index_minus_one_x)]
        edges_values_x = np.array(list(complex_x.loc[complex_x["edge_birth_index"] != -1, "value"]))
        distance_matrix_x = distances[0]
        complex_z = simplices[1]
        # We sort out the points on the diagonal on the persistence diagrams
        dying_simplicies_index_z = complex_z.loc[complex_z["edge_death_index"] != -1, "index"]
        dying_simplicies_index_minus_one_z = dying_simplicies_index_z - 1
        complex_z = complex_z[~complex_z["index"].isin(dying_simplicies_index_minus_one_z)]
        edges_values_z = np.array(list(complex_z.loc[complex_z["edge_birth_index"] != -1, "value"]))
        # Sorting out simplical complexes which are not edges (have no edge_birth_index)
        distance_matrix_z = distances[1]
        # Getting the combinations to calculate the loss from X to Z, and vice versa.
        edge_dist_x_x = distance_matrix_x[edges_values_x[:, 0], edges_values_x[:, 1]]
        edge_dist_z_z = distance_matrix_z[edges_values_z[:, 0], edges_values_z[:, 1]]
        edge_dist_x_z = distance_matrix_z[edges_values_x[:, 0], edges_values_x[:, 1]]
        edge_dist_z_x = distance_matrix_x[edges_values_z[:, 0], edges_values_z[:, 1]]

        distance1_2 = np.sum((np.square(edge_dist_x_x - edge_dist_x_z)))
        distance2_1 = np.sum(np.square(edge_dist_z_z - edge_dist_z_x))
        if distance1_2 == distance2_1:
            print("The parts of the symmetric topological are the same, perfect encoder/decoder?!")
        distance = distance1_2 + distance2_1

        return distance

    def forward(self, x):
        """Computes the loss of the topological autoencoder.
        :param x: Input tensor
        :type x: torch.Tensor
        :return: The cumulative loss (MSELoss + topological loss)
        :rtype: float
        """

        # Here we get the "normal" loss from the (always instantiated) autoencoder
        autoencoder_loss_not_normed = self.autoencoder.forward(x)

        # Calculate the topological loss
        latent_tensor = self.autoencoder.encode_into_latent_space(x)
        topological_loss_not_normed = self._calculate_topological_distance(x, latent_tensor)

        # normalize topological_loss according to batch_size
        batch_size = x.size()[0]
        topological_loss = topological_loss_not_normed / batch_size
        autoencoder_loss = autoencoder_loss_not_normed / batch_size
        print(f"{autoencoder_loss=}")
        print(f"{topological_loss * self.regularization_lambda=}")
        # Calculate the FINAL loss
        cumulative_loss = autoencoder_loss + self.regularization_lambda * topological_loss
        return cumulative_loss

    def encode_into_latent_space(self, x):
        """Computes the latent representation using our autoencoder.
        :param x: input data in space X
        :type x: torch.Tensor
        :return: output data in space Z
        :rtype: torch.Tensor
        """
        return self.autoencoder.encode_into_latent_space(x)

    def decode_from_latent_space(self, z):
        """Compute the reconstruction using our autoencoder.
        :param z: Input data in space Z
        :type z: torch.Tensor
        :return: Output data in space X
        :rtype: torch.Tensor
        """
        return self.autoencoder.decode_from_latent_space(z)


class TopologicalLayer(object):
    """Topological Layer WHICH I SKIPPED ENTIRELY"""

    def __init__(self):
        raise NotImplementedError

    def fit(self):
        raise NotImplementedError

    def transform(self):
        raise NotImplementedError

    def predict(self):
        raise NotImplementedError


def visualize_topological_autoencoder():
    """Visualizes the results of the TopologicalAutoencoder class. We use a fully connected autoencoder as skeleton.
    :return: None
    :rtype: None
    """
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    blobs_coord, blobs_label = make_blobs(n_samples=50, n_features=3, random_state=0)
    # Load and split data with a method from scikit-learn
    data_loader_train = torch.utils.data.DataLoader(blobs_coord, batch_size=4, shuffle=True, num_workers=4)
    topological_autoencoder = TopologicalAutoencoder()

    optimizer = optim.SGD(topological_autoencoder.parameters(), lr=0.1, momentum=0.9)
    lambda1 = lambda epoch: max(0.95 ** epoch, 0.00001 / 0.1)
    scheduler = LambdaLR(optimizer, lr_lambda=lambda1)
    # for real application: Move to GPU
    # topological_autoencoder.to(device)
    for epoch in range(50):  # loop over the dataset multiple times
        running_loss = 0.0
        for i, data in enumerate(data_loader_train):
            # get the inputs; data is a list of [inputs, labels]
            # for real application: Move to GPU
            # inputs, labels = data[0].to(device), data[1].to(device)
            if device == 'cuda':
                data = data.cuda(non_blocking=True)
            # forward + backward + optimize
            loss = topological_autoencoder(data.float())
            # zero the parameter gradients
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            # stats printing
            running_loss += loss.item()
            if i % 2000 == 1999:  # print every 2000 mini-batches
                print(f'[{epoch + 1}, {i + 1:5d}] loss: {running_loss / 2000:.3f}')
                running_loss = 0.0
        scheduler.step()

    print('Finished Training')
    # Visualizing
    encoded_data = topological_autoencoder.encode_into_latent_space(torch.tensor(blobs_coord).float())
    encoded_data_df = pandas.DataFrame(encoded_data.detach().cpu().numpy(), columns=["x", "y"])

    blobs_df = pandas.DataFrame(blobs_coord, columns=["x", "y", "z"])
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Blobs orig", "Encoding in 2D"),
                        specs=[[{"type": "scatter3d"}, {"type": "scatter"}]])
    fig.add_trace(
        go.Scatter3d(x=blobs_df["x"], y=blobs_df["y"], z=blobs_df["z"], mode="markers"),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=encoded_data_df["x"], y=encoded_data_df["y"], mode="markers"),
        row=1, col=2
    )

    fig.update_layout(title_text="Blobs and their encoded values in space Z")
    fig.show()
    fig.write_image("topological_autoencoder_final.png", width=1400, height=1000)


if __name__ == "__main__":
    visualize_topological_autoencoder()
