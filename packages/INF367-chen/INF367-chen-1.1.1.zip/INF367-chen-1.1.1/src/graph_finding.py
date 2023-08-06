"""Graph finding classes"""

import copy

import networkx as nx
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.spatial import Delaunay
from scipy.special import erf
from scipy.stats import multivariate_normal
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split

"""Implementation of different topological neural networks"""


class SelfOrganizingMap(object):
    """Self organizing map. For an example run, we refer to the method visualize_self_organizing_map()."""

    def __init__(self, length: int = 7, width: int = 9, random_state: int = 0):
        self._length = length
        self._width = width
        # Use initial random weights on fixed random state
        self._random_generator = np.random.RandomState(random_state)
        # Have to wait with proper initialization
        self._self_organizing_map = nx.grid_2d_graph(self._length, self._width)
        self._learning_rate = None
        self._neighbour_learning_rate = None

    def get_som(self):
        """Getter function
        @return: self-organizing map
        @rtype: nx.Graph
        """
        return self._self_organizing_map

    def _find_bmu_for_point(self, sample):
        """Finds the bmu (best matching unit) for the sample
        :param sample: sample of interest
        :type sample: np.array
        :return: (bmu x-corrdinate, bmu y-corrdinate)
        :rtype: Tuple(float, float)
        """
        # Euclidean distance between the rows/points in the training date and the centroids
        dist = [np.square(sample - attributes["vector"]).sum(axis=1) for node, attributes in
                self._self_organizing_map.nodes(data=True)]
        dist_as_array = np.array(dist).reshape(self._length, self._width)
        # Getting coordinates of the best matching unit
        bmu_x, bmu_y = np.argwhere(dist_as_array == np.min(dist_as_array))[0]
        return bmu_x, bmu_y

    def fit(self, training_data=None, learning_rate=0.5, learning_rate_decay=0.0001, neighbour_learning_rate=0.95,
            number_of_epochs=500):
        """Fits a self organizing map to the input training data.
        :param training_data: Training data
        :type training_data: np.array
        :param learning_rate: learning rate coefficient
        :type learning_rate: float
        :param learning_rate_decay: learning rate decay coefficient
        :type learning_rate_decay: float
        :param neighbour_learning_rate: neighbour learning rate decay coefficient
        :type neighbour_learning_rate: float
        :param number_of_epochs: training epoch number
        :type number_of_epochs: int
        :return: None
        :rtype: None
        """
        self._learning_rate = learning_rate
        self._neighbour_learning_rate = neighbour_learning_rate
        assert training_data is not None
        # Initialize the SOM around the mean of the training data
        random_indices_sample = self._random_generator.choice(range(training_data.shape[0]),
                                                              (self._length, self._width))
        init_data = training_data[random_indices_sample]
        for idx, (node, attributes) in enumerate(self._self_organizing_map.nodes(data=True)):
            attributes["vector"] = init_data[node]
        for epoch in range(number_of_epochs):
            print(f"Epoch {epoch} started...")
            # This shuffle fix was super for the performance of the SOM! We now do not always iterate in the same
            # way over the data points, which caused a bias in the direction of the last part of the training set
            self._random_generator.shuffle(training_data)
            for idx, sample in enumerate(training_data):
                bmu_x, bmu_y = self._find_bmu_for_point(training_data[idx].reshape(1, -1))
                # move the bmu (best matching unit)
                self._self_organizing_map.nodes[(bmu_x, bmu_y)]["vector"] += self._learning_rate * (
                        sample - self._self_organizing_map.nodes[(bmu_x, bmu_y)]["vector"])
                # move the neighbours of the bmu
                for neighbour_node in self._self_organizing_map.neighbors((bmu_x, bmu_y)):
                    self._self_organizing_map.nodes[neighbour_node][
                        "vector"] += np.multiply(np.multiply(self._learning_rate, self._neighbour_learning_rate), (
                            sample - self._self_organizing_map.nodes[neighbour_node]["vector"]))
            # Update rates
            self._learning_rate = self._learning_rate * np.exp(-epoch * learning_rate_decay)
            print(f"{self._learning_rate=}")
        print('Fitting finished\n')

    def transform(self, testing_data):
        """Computes euclidean distance between the closest center in the
        SOM and returns the corresponding labels for the input data.
        :param testing_data: Input testing data
        :type testing_data: np.array
        :return: Labels corresponding to the closest center in the SOM
        :rtype: List[int]
        """
        test_labels = []
        for point in testing_data:
            bmu_x, bmu_y = self._find_bmu_for_point(point)
            test_labels.append(np.array(bmu_x, bmu_y))
        return test_labels


class NeuralGas(object):
    """Neural Gas. Thought we can use it for the Growing Neural Gas...
    For an example run, we refer to the method visualize_neural_gas()."""

    def __init__(self):
        self._centers = None

    def fit(self, training_data, k, number_of_epochs, epsilon_start, epsilon_end,
            lambda_start, lambda_end, rand_seed):
        """Fits given number of centers to the training data via the Neural Gas algorithm.
        :param training_data: Training data
        :type training_data: np.array
        :param k: number of centers/clusters
        :type k: int
        :param number_of_epochs: Number of repetition steps in the algorithms
        :type number_of_epochs: int
        :param epsilon_start: Start value for the decreasing linear coefficient epsilon
        :type epsilon_start: float
        :param epsilon_end: Finishing value for the decreasing linear coefficient epsilon
        :type epsilon_end: float
        :param lambda_start: Start value for the decreasing linear coefficient lambda
        :type lambda_start: float
        :param lambda_end: Finishing value for the decreasing linear coefficient lambda
        :type lambda_end: float
        :param rand_seed: Random seed number for reproduction
        :type rand_seed: int
        :return:
        :rtype:
        """
        # we retrieve the sample size and the dimension/features
        n_samples, n_features = np.shape(training_data)
        # Set seed in the beginning (I think that is the same as when I fix the RandomState)
        np.random.seed(rand_seed)
        # randomly initialize centers
        self._centers = np.array(4 * np.random.rand(k, n_features) - 2)

        # with yield we can return values without stopping the functions workflow, here we return the initialisation
        yield copy.deepcopy(self._centers)
        for epoch in range(number_of_epochs):

            # This kind of slowing down the learning rate is much more elegant, since we can stop at a certain value
            learning_rate = epsilon_start * (epsilon_end / epsilon_start) ** (epoch / number_of_epochs)
            neighborhood_radius = lambda_start * (lambda_end / lambda_start) ** (epoch / number_of_epochs)

            print('Starting epoch t={} [learning rate={:.3f}, neighborhood radius = {:.3f}]...'.format(epoch,
                                                                                                       learning_rate,
                                                                                                       neighborhood_radius))

            # Either permutation or shuffle
            indexes = np.random.permutation(n_samples)

            # iterate through all indexes in the index array
            for index in indexes:
                sample = training_data[index]

                # Neural Gas learning rule is soft-competition, meaning that closer points will be moved more, but not
                # just the winner
                list_closest = np.argsort(np.linalg.norm(self._centers - sample, axis=1))
                for rank, closest in enumerate(list_closest, 0):
                    # This one was tricky, I had to transpose the sample
                    # to match the dimensions (we multiply point-wise)
                    self._centers[closest] += learning_rate * np.exp(-rank / neighborhood_radius) * (
                            np.transpose(sample) - self._centers[closest])

            # Convenience return for testing
            yield copy.deepcopy(self._centers)

        print('Fitting finished\n')

    def transform(self, sample):
        """Computes euclidean distance between the closest center in the
        Neural Gas and returns the corresponding label for the input sample.
        :param sample: Sample input
        :type sample: np.array
        :return: Label corresponding to the center
        :rtype: int
        """
        # Return the closest center
        list_closest = np.argsort(np.linalg.norm(self._centers - sample, axis=1))
        return list_closest[0]


class GrowingNeuralGas(object):
    """Growing Neural Gas. For an example run, we refer to the method visualize_growing_neural_gas()."""

    def __init__(self):
        self.node_number = 0
        self._graph = nx.Graph()
        np.random.seed(0)
        self.training_data = None

    def get_graph(self):
        """Getter function
        :return: Graph that is a representation of the Growing Neural Gas
        :rtype: nx.Graph
        """
        return self._graph

    def _get_next_node_number(self):
        """Internal counter which ensures unique node numbers starting with 0
        :return: current node number
        :rtype: int
        """
        self.node_number += 1
        return self.node_number - 1

    def fit(self, training_data, learning_rate_alpha=0.1, number_of_epochs: int = 25,
            number_of_steps_before_node_insertion=100, error_decay_beta=0.1, error_decay_gamma=0.1,
            age_threshold=50):
        """Fits the training data onto a nx.graph the represents the Growing Neural Network.
        :param training_data: Training data input
        :type training_data: np.array
        :param learning_rate_alpha: Learning rate of the linear coefficient alpha
        :type learning_rate_alpha: float
        :param number_of_epochs: Number of repetition steps in the algorithms
        :type number_of_epochs: int
        :param number_of_steps_before_node_insertion: Number of steps before a new node is inserted
        :type number_of_steps_before_node_insertion: int
        :param error_decay_beta: decaying coefficient beta
        :type error_decay_beta: float
        :param error_decay_gamma: decaying coefficient gamma
        :type error_decay_gamma: float
        :param age_threshold: Age threshold where edges above this threshold are eliminated
        :type age_threshold: int
        :return: None
        :rtype: None
        """
        self.training_data = training_data
        # Get the number of samples and their dimension
        n_samples, n_features = np.shape(self.training_data)
        # Add the two initial nodes
        w_one = 5 * np.random.rand(1, n_features) - 2.5
        w_two = 5 * np.random.rand(1, n_features) - 2.5
        # Initialize GNG with two connected nodes (edge age 0) with random weight vectors and errors 0
        self._graph.add_node(self._get_next_node_number(), vector=w_one, error=0)
        self._graph.add_node(self._get_next_node_number(), vector=w_two, error=0)
        # Adding initial edge
        # 0. epoch
        yield copy.deepcopy(self._graph)
        for epoch in range(number_of_epochs):
            print(f"Begin epoch {epoch}/{number_of_epochs}")
            # Either permutation or shuffle
            indexes = np.random.permutation(n_samples)
            running_steps = 0
            # iterate through all indexes in the index array
            for index in indexes:
                sample = training_data[index]
                # find two nearest vectors
                vec_1, vec_2 = self.find_the_two_closest_weight_vectors(sample)
                # add error, note that the Error in the pseudocode of the paper is SQUARED!
                self._graph.nodes[vec_1]['error'] += np.linalg.norm(sample - self._graph.nodes[vec_1]['vector']) ** 2
                # Update weights of vec_1 and vec_2, following the lecture slides, not the paper!!!
                # print(self._graph.nodes[vec_1]['vector'])
                self._graph.nodes[vec_1]['vector'] = np.add(self._graph.nodes[vec_1]['vector'],
                                                            learning_rate_alpha * np.subtract(sample,
                                                                                              self._graph.nodes[vec_1][
                                                                                                  'vector']))
                self._graph.nodes[vec_2]['vector'] = np.add(self._graph.nodes[vec_2]['vector'],
                                                            learning_rate_alpha * np.subtract(sample,
                                                                                              self._graph.nodes[
                                                                                                  vec_2]['vector']))
                # Increment age from all neighbour-edges of vec_1,
                # nbunch as argument allows filtering by the node in the graph (can be empty!)
                for node_1, neighbour_of_node_1, attributes in self._graph.edges(data=True, nbunch=[vec_1]):
                    # In the 0. epoch, we will not get here, since the graph has no edges yet
                    # add_edge is idempotent and will just overwrite the existing edge (updating)
                    self._graph.add_edge(node_1, neighbour_of_node_1, age=attributes['age'] + 1)
                # add edge between vec_1 and vec_2, set age to 0
                self._graph.add_edge(vec_1, vec_2, age=0)
                # delete nodes without edges, and edges that are too old
                self.kill_old_edges(age_threshold)
                self.kill_single_nodes()
                # Every m steps
                running_steps += 1
                if running_steps % number_of_steps_before_node_insertion == 0:
                    # Find node with largest error
                    biggest_error_node, max_error = 0, 0
                    for node, attributes in self._graph.nodes(data=True):
                        if attributes["error"] > max_error:
                            biggest_error_node = node
                            max_error = attributes["error"]
                    # Getting the neighbour with the highest error
                    neighbour_error_dict = {}
                    for neighbour in self._graph.neighbors(biggest_error_node):
                        neighbour_error_dict[neighbour] = (self._graph.nodes[neighbour]['error'])
                    # Get the neighbour with the biggest error
                    (biggest_error_neighbour_node, biggest_error_neighbour_error) = \
                        list(sorted(neighbour_error_dict.items(), key=lambda x: x[1], reverse=True))[0]  # type: ignore
                    # Update error of the two vectors
                    self._graph.nodes[biggest_error_node]['error'] *= error_decay_beta
                    self._graph.nodes[biggest_error_neighbour_node]['error'] *= error_decay_beta
                    # Delete edge between them
                    self._graph.remove_edge(biggest_error_node, biggest_error_neighbour_node)
                    # Add new node
                    new_node = (self._graph.nodes[biggest_error_node]["vector"] +
                                self._graph.nodes[biggest_error_neighbour_node]["vector"]) * 0.5
                    new_node_number = self._get_next_node_number()
                    self._graph.add_node(new_node_number,
                                         vector=new_node,
                                         error=self._graph.nodes[biggest_error_node]['error'])
                    # Add edges
                    self._graph.add_edge(new_node_number, biggest_error_node, age=0)
                    self._graph.add_edge(new_node_number, biggest_error_neighbour_node, age=0)

                for node, attributes in self._graph.nodes(data=True):
                    attributes["error"] = attributes["error"] * error_decay_gamma
                yield copy.deepcopy(self._graph)
        print('Fitting finished\n')

    def transform(self, sample):
        """Returns the closest center of the GNG
        :param sample: The sample of interest
        :type sample: np.array
        :return: The closest node/center
        :rtype: int
        """
        two_closest = self.find_the_two_closest_weight_vectors(sample)
        return two_closest[0]

    def find_the_two_closest_weight_vectors(self, sample):
        """Finds the closest two centers to the sample
        :param sample: The sample of interest
        :type sample: np.array
        :return: The two closest centers to the sample in the format (node number 1, node number 2).
        :rtype: Tuple[int, int]
        """
        # Get a ranking of which weight vectors are closest.
        all_graph_weight_vectors = {node_number: attributes['vector'].flatten() for node_number, attributes in
                                    self._graph.nodes(data=True)}
        distances = {k: np.linalg.norm(v - sample) for k, v in all_graph_weight_vectors.items()}
        list_closest = list(sorted(distances.items(), key=lambda x: x[1]))[:2]  # type: ignore

        # return the nearest and second closest point
        return list_closest[0][0], list_closest[1][0]

    def kill_single_nodes(self):
        to_be_deleted = []
        # So messy! But we have to iterate through the nodes first to determine which ones to
        # delete before actually deleting them, otherwise the for loops break
        for node in self._graph.nodes:
            if self._graph.degree(node) == 0:
                to_be_deleted.append(node)
        for node in to_be_deleted:
            self._graph.remove_node(node)

    def kill_old_edges(self, age_threshold):
        to_be_deleted = []
        # Same as for the elimination of nodes. Messy workaround.
        for node_1, neighbour_of_node_1, attributes in self._graph.edges(data=True):
            if attributes['age'] > age_threshold:
                to_be_deleted.append((node_1, neighbour_of_node_1))
        for node, other_node in to_be_deleted:
            self._graph.remove_edge(node, other_node)


class GenerativeGaussianGraph(object):
    """Generative Gaussian Graphs. For an example run, we refer to the method visualize_generative_gaussian_graph()"""

    def __init__(self):
        self._graph = nx.Graph()

    def get_graph(self):
        """Getter function
        :return: Graph that is a representation of the Generative Gaussian Graph
        :rtype: nx.Graph
        """
        return self._graph

    def fit(self, training_data, ng_number_of_components_k=10, ng_number_of_epochs=50, ng_epsilon_start=1,
            ng_epsilon_end=0.001,
            ng_lambda_start=15, ng_lambda_end=0.001, ng_rand_seed=0, pruning_threshold_epsilon=0.01):
        """Not finished Implementation of the the fit function for the Generative Gaussian Graph.
        :param training_data: Training data input
        :type training_data: np.array
        :param ng_number_of_components_k: Number of components for the Neural Gas algorithm
        :type ng_number_of_components_k: int
        :param ng_number_of_epochs: Number of training epochs for the Neural Gas algorithm
        :type ng_number_of_epochs: int
        :param ng_epsilon_start: Starting number of neighbourhood coefficient for the Neural Gas algorithm
        :type ng_epsilon_start: float
        :param ng_epsilon_end: Ending number of neighbourhood coefficient for the Neural Gas algorithm
        :type ng_epsilon_end: float
        :param ng_lambda_start: Starting number of weight coefficient for the Neural Gas algorithm
        :type ng_lambda_start: float
        :param ng_lambda_end: Starting number of weight coefficient for the Neural Gas algorithm
        :type ng_lambda_end: float
        :param ng_rand_seed: Seed number for reproduction
        :type ng_rand_seed: int
        :param pruning_threshold_epsilon: Threshold for pruning edges in the Generative Gaussian Graphs
        :type pruning_threshold_epsilon: float
        :return: None
        :rtype: None
        """
        # Step 1: Get centers via vector quantization
        # We follow the original pseudocode from the paper, in which the vector quantization is done with neural gas
        ng = NeuralGas()
        centers_from_last_epoch = np.array(
            list(ng.fit(training_data, ng_number_of_components_k, ng_number_of_epochs, ng_epsilon_start, ng_epsilon_end,
                        ng_lambda_start, ng_lambda_end, ng_rand_seed)))[-1]
        # Step 2: Delaunay graph
        tri = Delaunay(centers_from_last_epoch)
        # Add nodes
        for idx, vector in enumerate(tri.points):
            self._graph.add_node(idx, vector=vector)
        # Add edges
        for node_1, node_2, node_3 in tri.simplices:
            self._graph.add_edges_from([(node_1, node_2), (node_1, node_3), (node_2, node_3)])
        print(self._graph)
        yield self._graph
        # Step 3: Initialize density model
        initial_probability = 1 / (len(self.get_graph().nodes) + len(self.get_graph().edges))
        sigma_squared = 1
        counter = 0
        while counter < 5:
            for node, attributes in self._graph.nodes(data=True):
                attributes["pi"] = initial_probability
                # attributes["sigma"] = 1
                # attributes["center_label"] = ng.transform(attributes["vector"])
                print(f"Weight for {node=} set to {initial_probability}")
            for (node_1, node_2, attributes) in self._graph.edges(data=True):
                attributes["pi"] = initial_probability
                # attributes["sigma"] = 1
                print(f"Weight pi for edge between {node_1=} and { node_2=} set to {initial_probability}")
            # Step 4: Optimize likelihood (EM)
            # Basically matrix N x M with N data points and M centers, probabilities as the values
            # Co variance matrix is just Identity * sigma
            # We use the weights w instead of the mean (as in GMM) in the E and M steps
            dimension_d = 2  # Just as reminder
            # E-step
            # Calculate probability of the point that it is in one specific cluster:
            for node, attributes in self._graph.nodes(data=True):
                distribution = multivariate_normal(mean=attributes["vector"], cov=sigma_squared)
                prob_in_nodes = distribution.pdf(training_data)
                # Only for debugging
                # print(prob_in_nodes)
            # Calculate probability of the point that it is in one specific edge cluster:
            prob_in_edges = []
            for datum in training_data:
                for (node_1, node_2, attributes) in self._graph.edges(data=True):
                    if node_1 == node_2:
                        prob_in_edges.append(
                            multivariate_normal.pdf(datum, mean=attributes["vector"], cov=sigma_squared))
                    node_1_vector = self._graph.nodes(data=True)[node_1]["vector"]
                    node_2_vector = self._graph.nodes(data=True)[node_2]["vector"]
                    l_a_b_norm = np.linalg.norm(node_1_vector - node_2_vector)  # one dimensional
                    qj_aibi = np.dot(datum - node_1_vector, node_2_vector - node_1_vector) / l_a_b_norm
                    q_ij = node_1_vector + (node_2_vector - node_1_vector) * (qj_aibi / l_a_b_norm)

                    first_factor = np.exp(
                        - np.dot(datum - q_ij, datum - q_ij) / (
                                (2 * np.pi * sigma_squared) ** ((dimension_d - 1) / 2)))
                    second_factor = (erf(qj_aibi / np.sqrt(sigma_squared) * np.sqrt(2)) - erf(
                        qj_aibi - l_a_b_norm / (sigma_squared) * np.sqrt(2))) / (2 * l_a_b_norm)
                    prob_in_edges.append(first_factor * second_factor)
            # Only for debugging
            # print(prob_in_edges)
            # M-step
            # calculate big M as the number of edges AND nodes
            big_m = len(training_data)
            # Update weight: Nodes
            m_factor = 1 / big_m
            for node, attributes in self._graph.nodes(data=True):
                m_sum = 0
                for idx, datum in enumerate(training_data):
                    # getting gaussian mixture
                    gaussian_sum = 0
                    for node, attributes in self._graph.nodes(data=True):
                        gaussian_sum += attributes["pi"] * prob_in_nodes[idx]
                    for (node_1, node_2, attributes) in self._graph.edges(data=True):
                        gaussian_sum += attributes["pi"] * prob_in_edges[idx]
                    m_sum += attributes["pi"] * prob_in_nodes[idx] / gaussian_sum
                attributes["pi_new"] = m_factor * m_sum
                print(f"New pi: {attributes['pi_new']}")
            # Update weight: Edges
            m_sum = 0
            for (node_1, node_2, attributes) in self._graph.edges(data=True):
                for idx, datum in enumerate(training_data):
                    # getting gaussian mixture
                    gaussian_sum = 0
                    for node, attributes in self._graph.nodes(data=True):
                        gaussian_sum += attributes["pi"] * prob_in_nodes[idx]
                    for (node_1, node_2, attributes) in self._graph.edges(data=True):
                        gaussian_sum += attributes["pi"] * prob_in_edges[idx]
                    m_sum += attributes["pi"] * prob_in_nodes[idx] / gaussian_sum
                attributes["pi_new"] = m_factor * m_sum
                print(f"New pi: {attributes['pi_new']}")
            # Update sigma:
            prefactor = 1 / (dimension_d * big_m)
            i_1 = sigma_squared * np.sqrt((np.pi / 2)) * (erf(qj_aibi / ((sigma_squared) * np.sqrt(2))) - erf(
                (qj_aibi - l_a_b_norm) / ((sigma_squared) * np.sqrt(2))))
            i_2 = sigma_squared * ((qj_aibi - l_a_b_norm) * np.exp(
                -(np.square(qj_aibi - l_a_b_norm) / 2 * sigma_squared)) - qj_aibi * np.exp(
                -(np.square(qj_aibi) / 2 * sigma_squared)))
            sum_total = 0
            for idx, datum in enumerate(training_data):
                # getting gaussian mixture
                middle_sum = 0
                for node, attributes in self._graph.nodes(data=True):
                    middle_sum += attributes["pi"] * prob_in_nodes[idx] * np.square(
                        prob_in_nodes[idx] - attributes["vector"])
                for (node_1, node_2, attributes) in self._graph.edges(data=True):
                    big_addendum_upper = (2 * attributes["pi"]) ** (-dimension_d / 2) * np.exp(
                        -np.square(prob_in_nodes[idx] - q_ij) / (2 * prob_in_nodes[idx] ** 2)) * (
                                                 i_1 * (
                                                 ((np.square(prob_in_nodes[idx] - q_ij)) ** 2) + sigma_squared) + i_2)
                    big_addendum_lower = l_a_b_norm * prob_in_edges[idx]
                    big_addendum = big_addendum_upper / big_addendum_lower
                    middle_sum += attributes["pi"] * prob_in_edges[idx] * big_addendum
                sum_total += middle_sum

            sigma_new = prefactor * sum_total
            print(f"New sigma: {sigma_new}")
            # Overwrite old values with the new ones:
            for node, attributes in self._graph.nodes(data=True):
                attributes["pi"] = attributes["pi_new"]
            for (node_1, node_2, attributes) in self._graph.edges(data=True):
                attributes["pi"] = attributes["pi_new"]
            sigma_squared = sigma_new
            counter += 1
        raise NotImplementedError("Only done stuff up til here for GGG!!!")
        # Step 5: Prune graph

        # pi: weights which sum up to 1
        # v underlying data.
        # mean is mu, noise is sigma2
        # Gaussian Kernel: Either Gaussian point (node) or gaussian segment (edge)
        # w prototype with variance (gaussian kernel!!)
        # Optimize for PI and SIGMA2

def draw_moons(fig, moon_train_coord, moon_test_coord, label_train, label_test):
    """Draws the two moons example from sklearn.
    :param fig: Incoming plotly figure
    :type fig: plotly.figure
    :param moon_train_coord: training moon coordinates to be drawn
    :type moon_train_coord: np.array
    :param moon_test_coord: test moon coordinates to be drawn
    :type moon_test_coord: np.array
    :param label_train: labels of the training moon coordinates
    :type label_train: np.array
    :param label_test: labels of the test moon coordinates
    :type label_test: np.array
    :return: None
    :rtype: None
    """
    training_and_test_traces = [
        [moon_train_coord, label_train, '0', 'Train', 'square', 'blue'],
        [moon_train_coord, label_train, '1', 'Train', 'circle', 'red'],
        [moon_test_coord, label_test, '0', 'Test', 'square-dot', 'blue'],
        [moon_test_coord, label_test, '1', 'Test', 'circle-dot', 'red'],
    ]

    # Plotly has the nice ability to just "add" traces to an existing plot which
    # we have defined as training_and_test_traces
    for _moon_coord, _moon_label, _iterating_label, _split, _marker, _color in training_and_test_traces:
        fig.add_trace(
            go.Scatter(
                x=_moon_coord[_moon_label == _iterating_label, 0],
                y=_moon_coord[_moon_label == _iterating_label, 1],
                name=f'{_split} Split, Label {_iterating_label}',
                mode='markers', marker=dict(symbol=_marker, color=_color, opacity=0.5)
            ))
    fig.update_traces(
        marker_size=11, marker_line_width=1.2,
    )


def visualize_self_organizing_map():
    """Visualizes self-organizing maps via plotly. Produces som_final.png as output.
    :return: None
    :rtype: None
    """
    som = SelfOrganizingMap()
    moon_coord, moon_label = make_moons(n_samples=250, noise=0.02, random_state=0)
    # Load and split data with a method from scikit-learn
    moon_train_coord, moon_test_coord, label_train, label_test = train_test_split(
        moon_coord, moon_label.astype(str), test_size=0.25, random_state=0)
    som.fit(moon_train_coord)

    edge_x = []
    edge_y = []
    for edge in som.get_som().edges():
        x0, y0 = som.get_som().nodes[edge[0]]['vector'].flatten().tolist()
        x1, y1 = som.get_som().nodes[edge[1]]['vector'].flatten().tolist()
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    node_x = []
    node_y = []
    for node in som.get_som().nodes():
        x, y = som.get_som().nodes[node]['vector'].flatten().tolist()
        node_x.append(x)
        node_y.append(y)
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        name="Edges",
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        name="Nodes",
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))
    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(som.get_som().adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append('# of connections: ' + str(len(adjacencies[1])))

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='SOM on the two moons',
                        titlefont_size=16,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        annotations=[dict(
                            text="Author: I-Hao Chen",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002)],
                        legend=dict(
                            yanchor="top",
                            y=0.99,
                            xanchor="left",
                            x=0.01)
                    ))
    draw_moons(fig, moon_train_coord, moon_test_coord, label_train, label_test)
    fig.show()
    fig.write_image("som_final.png", width=1400, height=1000)


def visualize_neural_gas():
    """Visualizes Neural Gas via plotly.
    :return: None
    :rtype: None
    """
    # hyperparameters for neural gas
    k = 25
    number_of_epochs = 50
    epsilon_start = 1
    epsilon_end = 0.001
    lambda_start = 15
    lambda_end = 0.001

    # seed
    rand_seed = 0

    moon_coord, moon_label = make_moons(n_samples=250, noise=0.02, random_state=0)
    # Load and split data with a method from scikit-learn
    moon_train_coord, moon_test_coord, label_train, label_test = train_test_split(
        moon_coord, moon_label.astype(str), test_size=0.25, random_state=0)
    ng = NeuralGas()
    results = np.array(list(ng.fit(moon_train_coord, k, number_of_epochs, epsilon_start, epsilon_end,
                                   lambda_start, lambda_end, rand_seed)))
    # We want to visualize the algorithm with an animation, so we need pandas and DataFrames to do so
    col_names = ['epoch', 'cluster_label', 'coordinates']
    # Creates our index for MultiIndex later
    index = pd.MultiIndex.from_product([range(s) for s in results.shape], names=col_names)
    # Creates a series with all the values and holding on to the correct epoch via the Multiindex
    df = pd.DataFrame({'results_list': results.flatten()}, index=index)['results_list']
    df = df.unstack(level='coordinates').swaplevel().sort_index()
    df.columns = ['x', 'y']
    df.index.names = ['cluster_label', 'epoch']
    df = df.reset_index()
    fig = px.scatter(df, x="x", y="y", animation_frame="epoch", animation_group="cluster_label",
                     color="cluster_label", hover_name="cluster_label", range_x=[-2.5, 2.5], range_y=[-2.5, 2.5],
                     title="Neural Gas on the two moons")
    draw_moons(fig, moon_train_coord, moon_test_coord, label_train, label_test)
    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))
    fig.show()


def visualize_growing_neural_gas():
    """Visualizes Growing Neural Gas via plotly and tests it on one sample. Produces ggg_final.png as output.
    :return: None
    :rtype: None
    """
    moon_coord, moon_label = make_moons(n_samples=250, noise=0.02, random_state=0)
    # Load and split data with a method from scikit-learn
    moon_train_coord, moon_test_coord, label_train, label_test = train_test_split(
        moon_coord, moon_label.astype(str), test_size=0.25, random_state=0)
    gng = GrowingNeuralGas()
    results = list(gng.fit(moon_train_coord))
    print(f"{len(results)} steps in total trained!")
    edge_x = []
    edge_y = []
    for edge in gng.get_graph().edges():
        x0, y0 = gng.get_graph().nodes[edge[0]]['vector'].flatten().tolist()
        x1, y1 = gng.get_graph().nodes[edge[1]]['vector'].flatten().tolist()
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    node_x = []
    node_y = []
    for node in gng.get_graph().nodes():
        x, y = gng.get_graph().nodes[node]['vector'].flatten().tolist()
        node_x.append(x)
        node_y.append(y)
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines',
        name="Edges")
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        name="Nodes",
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))
    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(gng.get_graph().adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append('# of connections: ' + str(len(adjacencies[1])))

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='GNG on the two moons',
                        titlefont_size=16,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        annotations=[dict(
                            text="Author: I-Hao Chen",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002)],
                        legend=dict(
                            yanchor="top",
                            y=0.99,
                            xanchor="left",
                            x=0.01)
                    ))
    draw_moons(fig, moon_train_coord, moon_test_coord, label_train, label_test)
    fig.show()
    fig.write_image("gng_final.png", width=1400, height=1000)
    closest_center = gng.transform(moon_test_coord[0])
    print(f"Closest center to {moon_test_coord[0]} is node number: {closest_center}")


def visualize_generative_gaussian_graph():
    """Visualizes Generative Gaussian Graphs via plotly and tests it on one sample. Produces ggg_delauny_final.png as output.
    :return: None
    :rtype: None
    """
    moon_coord, moon_label = make_moons(n_samples=250, noise=0.02, random_state=0)
    # Load and split data with a method from scikit-learn
    moon_train_coord, moon_test_coord, label_train, label_test = train_test_split(
        moon_coord, moon_label.astype(str), test_size=0.25, random_state=0)
    ggg = GenerativeGaussianGraph()
    results = list(ggg.fit(moon_train_coord))
    print(f"{len(results)} steps in total trained!")
    edge_x = []
    edge_y = []
    for edge in ggg.get_graph().edges():
        x0, y0 = ggg.get_graph().nodes[edge[0]]['vector'].flatten().tolist()
        x1, y1 = ggg.get_graph().nodes[edge[1]]['vector'].flatten().tolist()
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    node_x = []
    node_y = []
    for node in ggg.get_graph().nodes():
        x, y = ggg.get_graph().nodes[node]['vector'].flatten().tolist()
        node_x.append(x)
        node_y.append(y)
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines',
        name="Edges")
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        name="Nodes",
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))
    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(ggg.get_graph().adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append('# of connections: ' + str(len(adjacencies[1])))

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Delauny on the two moons',
                        titlefont_size=16,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        annotations=[dict(
                            text="Author: I-Hao Chen",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002)],
                        legend=dict(
                            yanchor="top",
                            y=0.99,
                            xanchor="left",
                            x=0.01)
                    ))
    draw_moons(fig, moon_train_coord, moon_test_coord, label_train, label_test)
    fig.show()
    fig.write_image("ggg_delauny_final.png", width=1400, height=1000)


if __name__ == "__main__":
    visualize_self_organizing_map()
    visualize_neural_gas()
    visualize_growing_neural_gas()
    visualize_generative_gaussian_graph()
