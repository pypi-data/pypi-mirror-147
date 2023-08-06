"""Persistent Homology classes like PersistenceDiagram, PersistenceImage, PersistenceLandscape"""
from itertools import combinations

import numpy as np
import pandas
import plotly.express as px
import plotly.graph_objects as go
import torch
from plotly.subplots import make_subplots
from scipy.signal import convolve2d
from sklearn.datasets import make_moons
from sklearn.metrics import euclidean_distances
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KernelDensity

# Some example values from the youtube video about this topic for testing.
example_boundary_matrix = np.array([[0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                                    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0],
                                    [0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
example_boundary_matrix_dimensions = np.array([0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2])
example_distance_matrix = np.array([[0., 3.23398405, 3.23398405, 3.23398405, 3.23398405, 3.23398405],
                                    [0., 0., 3.23398405, 2.26929705, 2.73298802, 2.26929705],
                                    [0., 0., 0., 3.23398405, 3.23398405, 3.23398405],
                                    [0., 0., 0., 0., 2.7]])
example_reduced_matrix = np.array([[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

example_persistence_pairs = pandas.DataFrame(columns=["birth", "death", "dimension"],
                                             data=np.array(
                                                 [[0, np.inf, 0], [2, 4, 0], [3, 5, 0], [1, 6, 0], [8, 9, 1],
                                                  [7, 10, 1]]))


def get_mutual_reachability_distance_matrix(all_points: np.array, k_nearest_neighours=5):
    """Calculates the mutual reachability distance matrix
    :param all_points: Input points
    :type all_points: np.array
    :param k_nearest_neighours: Number of k nearest neighbours that should be used in the algorithm
    :type k_nearest_neighours: int
    :return: mutual reachability distance matrix
    :rtype: np.array
    """
    number_of_datapoints = len(all_points)
    distance_matrix = np.zeros((number_of_datapoints, number_of_datapoints))
    indices = list(combinations(range(number_of_datapoints), 2))
    for (id_1, id_2), (point_1, point_2) in zip(indices, combinations(all_points, 2)):
        distance_matrix[id_1, id_2] = mutual_reachability_distance(all_points, point_1, point_2, k_nearest_neighours)
    return distance_matrix


def mutual_reachability_distance(all_points: np.array, a, b, k_nearest_neighours=5):
    """Calcualtes the mutual_reachability_distance between two points a and b.
    :param all_points: All points in which a and b also are lying.
    :type all_points: np.array
    :param a: The first point of interest.
    :type a: np.array
    :param b: The second point of interest.
    :type b: np.array
    :param k_nearest_neighours: Number of k nearest neighbours that should be used in the algorithm
    :type k_nearest_neighours: int
    :return: distance between a and b in term of mutual reachability.
    :rtype: float
    """
    # calculate the core_k of a and b respectively
    a_core = np.sort(euclidean_distances(a.reshape(1, -1), np.array(all_points)).transpose().flatten().tolist())[
             1:k_nearest_neighours + 1]
    a_core_max = max(a_core) if len(a_core) > 0 else 0
    b_core = np.sort(euclidean_distances(b.reshape(1, -1), np.array(all_points)).transpose().flatten().tolist())[
             1:k_nearest_neighours + 1]
    b_core_max = max(b_core) if len(b_core) > 0 else 0
    # Calculate distance between a and b
    dist_a_b = euclidean_distances(a.reshape(1, -1), b.reshape(1, -1)).flatten()[0]
    # get the max of the three values
    max_value = max(a_core_max, b_core_max, dist_a_b)
    return max_value


def create_boundary_matrix_from_simplices_dataframe(df_simplices: pandas.DataFrame) -> tuple[np.array, np.array]:
    """Creats a boundary matrix from simplicies.
    :param df_simplices: The simplicies that will form the simplical complex.
    :type df_simplices: pandas.DataFrame
    :return: boundary matrix and the dimensions of it as a separate array.
    :rtype: Tuple[np.array, np.array]
    """
    print("Calculating boundary_matrix: This may take a while...")
    # Initialize boundary matrix
    boundary_matrix = np.zeros((len(df_simplices), len(df_simplices)), dtype=int)
    boundary_matrix_dimensions = np.zeros(len(df_simplices), dtype=int)
    list_over_all_indices = df_simplices["value"].tolist()
    for col_index, indices in enumerate(list_over_all_indices):
        # 0-dimensional simplices
        if len(indices) == 1:
            continue
        # Find the coordinates in the boundary matrix for the faces of n-1 dimension
        sub_dim = len(indices) - 1
        for comb in combinations(indices, sub_dim):
            for idx, row in enumerate(df_simplices["value"]):
                if list(comb) == row:
                    boundary_matrix[idx, col_index] = 1
                boundary_matrix_dimensions[idx] = df_simplices.iloc[idx]["dimension"]
        # fixing highest dimension

    # Small check for the validity of the boundary matrix
    assert np.all((boundary_matrix == 0) | (boundary_matrix == 1))
    print(f"Boundary Matrix: \n {boundary_matrix}")
    print(f"Boundary Matrix Dimensions: \n {boundary_matrix_dimensions}")
    return boundary_matrix, boundary_matrix_dimensions


class FilteredComplexes(object):
    """Filtered Complexes. For an example run, we refer to the method visualize_filtered_complex()."""

    def __init__(self, training_data: np.array = None):
        self.distance_list = None
        self._training_data = training_data
        self._index = 0
        self._edge_index = 0
        self._not_changed_counter = 0
        self._df_length = -1
        # Init of the simplices DataFrame
        self.df_simplices = pandas.DataFrame(
            columns=["index", "dimension", "value", "edge_birth_index", "edge_death_index"])

    def get_next_node_number(self):
        """Getter function
        @return: Current node number
        @rtype: int
        """
        self._index += 1
        return self._index - 1

    def get_next_edge_number(self):
        """Getter function
        @return: Current node number
        @rtype: int
        """
        self._edge_index += 1
        return self._edge_index - 1

    def get_simplices(self):
        """Getter function
        @return: simplicies
        @rtype: pandas.DataFrame
        """
        return self.df_simplices

    def _calculate_simplices(self, dist_matrix, max_simplices_dim, verbose=False):
        """Calculates internally simplicies based on distance matrix.
        :param dist_matrix: Distance matrix
        :type dist_matrix: np.array
        :param max_simplices_dim: Highest dimension of the simplicies that can be achieved
        :type max_simplices_dim: int
        :return: None
        :rtype: None
        """
        list_of_iterating_radius = np.sort(np.unique(dist_matrix.flatten()))
        print(f"All radii: {list_of_iterating_radius}")
        # saving distances for the barcode
        # Spreading radius
        for radius in list_of_iterating_radius:
            if verbose:
                print(f"The current radius is: {radius}")

            edges = np.where(dist_matrix <= radius, 1, 0)
            # This matrix contains 1 where we have an edge between datapoints for the given radius
            upper_matrix_with_edges = np.triu(edges, k=1)
            if verbose:
                print(upper_matrix_with_edges)
            # get the indices of the edge points
            edges_indices = np.argwhere(upper_matrix_with_edges == 1)
            if verbose:
                print(edges_indices)
            for dimension in range(1, max_simplices_dim + 1):
                if dimension == 1:
                    for edge in edges_indices.tolist():
                        if edge not in self.df_simplices[self.df_simplices["dimension"] == dimension]["value"].tolist():
                            self.distance_list.append(radius)  # saving the distance
                            new_df_row = dict(index=self.get_next_node_number(), dimension=dimension, value=edge,
                                              edge_birth_index=self.get_next_edge_number(), edge_death_index=-1)
                            new_df_row = pandas.DataFrame([new_df_row])
                            self.df_simplices = pandas.concat([self.df_simplices, new_df_row])
                else:
                    # All higher dimensions rely on looking up whether we have created such an index combination
                    # that the simplicy of dimnesion n has been created
                    all_combs_of_current_dimension = combinations(range(len(dist_matrix)), dimension + 1)
                    for comb in all_combs_of_current_dimension:
                        combinations_of_one_dimension_lower = combinations(comb, dimension)
                        matches_from_lower_dimension = 0
                        # Count if we have all the faces of n-1 dimension to build the simplex of dimension n
                        for comb_from_lower_dim in combinations_of_one_dimension_lower:
                            if list(comb_from_lower_dim) in \
                                    self.df_simplices[self.df_simplices["dimension"] == dimension - 1][
                                        "value"].tolist():
                                matches_from_lower_dimension += 1
                        # We got a simplex!
                        if matches_from_lower_dimension == dimension + 1:
                            if list(comb) not in self.df_simplices[self.df_simplices["dimension"] == dimension][
                                "value"].tolist():
                                self.distance_list.append(radius)  # saving the distance
                                if verbose:
                                    print(f"We got a {dimension}-dimensional simplex: {comb}")
                                new_df_row = dict(index=self.get_next_node_number(), dimension=dimension,
                                                  value=list(comb), edge_birth_index=-1,
                                                  edge_death_index=self.get_next_edge_number())
                                new_df_row = pandas.DataFrame([new_df_row])
                                self.df_simplices = pandas.concat([self.df_simplices, new_df_row])
            if verbose:
                print(self.df_simplices)
            self.df_simplices = self.df_simplices.set_index("index")
            self.df_simplices["index"] = self.df_simplices.index
        if verbose:
            print(f"Final dataframe of simplices is: {self.df_simplices}")

    def fit(self, max_simplices_dim: int = 3, k_nearest_neighours=5, own_dist_matrix=None):
        """Fits a Filtered Simplical Complex onto the training data.
        :param max_simplices_dim: Highest dimension of the simplicies that can be achieved
        :type max_simplices_dim: int
        :param k_nearest_neighours: Number of k nearest neighbours that should be used in the algorithm
        :type k_nearest_neighours: int
        :param own_dist_matrix: Usually none, sometimes we already have calculated one, then we can use it here.
        :type own_dist_matrix: np.array
        :return: Returns a boundary matrix, an array with the dimension of the persistence pairs,
        and then also a distance list where the actual distances between nodes are saved.
        :rtype: Tuple[np.array, np.array, List[float]]
        """
        # We fit via rips complex with HDBSCANs distance function mutual_reachability_distance
        self.distance_list = []
        # First we calculate the distance matrix (dist fucntion is the mutual reachability distance)
        if own_dist_matrix is not None:
            dist_matrix = own_dist_matrix
        else:
            dist_matrix = get_mutual_reachability_distance_matrix(self._training_data,
                                                                  k_nearest_neighours=k_nearest_neighours)
        # Add 0 dimensional simplices
        for idx, point in enumerate(range(len(dist_matrix))):
            self.distance_list.append(0)
            new_df_row = dict(index=self.get_next_node_number(), dimension=0, value=[idx], edge_birth_index=-1,
                              edge_death_index=-1)
            new_df_row = pandas.DataFrame([new_df_row])
            self.df_simplices = pandas.concat([self.df_simplices, new_df_row])

        self._calculate_simplices(dist_matrix, max_simplices_dim)
        boundary_matrix, dimensions_array = create_boundary_matrix_from_simplices_dataframe(self.df_simplices)
        assert len(dimensions_array) == len(self.distance_list), "Distance list is not filled properly!!"
        return boundary_matrix, dimensions_array, self.distance_list


def reduction_of_column(transposed_matrix, index_of_current_row):
    """Reduces the current column of a boundary matrix.
    :param transposed_matrix: The matrix to be reduced in transposed form
    :type transposed_matrix: np.array
    :param index_of_current_row: The column of interest
    :type index_of_current_row: int
    :return: transposed matrix with the reduced column
    :rtype: np.array
    """
    row_we_want_to_add = 0
    # We are in the while loop as long we have potential (now) rows to add to our current (now) row
    while row_we_want_to_add != -1:
        # if column (row now) contains only zeros, we skip it
        if np.all((transposed_matrix[index_of_current_row] == 0)):
            return transposed_matrix
        # we ask for the first value which is non-zero. In the transposed matrix, it is the last value in the (now) row.
        index = np.where(transposed_matrix[index_of_current_row] != 0)[0][-1]
        # we select here the matrix now rows up to the index of our column to check the previous ones
        cutted_matrix = transposed_matrix[:index_of_current_row]
        # get the column of interest
        column_of_interest = cutted_matrix[:, index]
        # get the index of the potentially lowest non zero element
        check_for_non_zeros = np.where(column_of_interest != 0)[0]
        # if that column has only zeros, then our now row has the lowest index value already!
        if np.all((check_for_non_zeros == 0)):
            return transposed_matrix
        # -1 indicates that there is no lowest non zero value (all are zero)
        row_we_want_to_add = check_for_non_zeros[-1] if len(check_for_non_zeros) > 0 else -1
        # Get the (lowest) latest non zero value in that now row
        lowest_index_of_the_row_we_want_to_add = np.where(transposed_matrix[row_we_want_to_add] != 0)[0][-1]
        # Check the the lowest non zero value index is actually the lowest one, or we will never finish!
        is_actually_lowest_equal = index == lowest_index_of_the_row_we_want_to_add
        if is_actually_lowest_equal:
            new_now_row = np.mod(np.add(transposed_matrix[row_we_want_to_add],
                                        transposed_matrix[index_of_current_row]), 2)
            transposed_matrix[index_of_current_row] = new_now_row
        else:
            break
    return transposed_matrix


class MatrixReduction(object):
    """Matrix Reduction. For an example run, we refer to the method visualize_matrix_reduction()."""

    def __init__(self, boundary_matrix: np.array, boundary_matrix_dimens: np.array, distance_list: np.array = None):
        self._bounday_matrix = boundary_matrix
        self._distance_list = distance_list
        self._boundary_matrix_dimens = boundary_matrix_dimens
        self._reduced_matrix = None
        self._persistence_pairs = pandas.DataFrame(columns=["birth", "death", "dimension"])
        self._reduced_matrix_barcode = pandas.DataFrame(columns=["birth_value", "death_value", "dimension"])

    def get_barcode_of_reduced_matrix(self):
        return self._reduced_matrix_barcode

    def get_persistence_pairs(self):
        return self._persistence_pairs

    def get_reduced_matrix(self):
        return self._reduced_matrix

    def _calculate_persistence_pairs_and_barcode(self):
        """The dimension are needed in a separate 1-dim np.array"""
        # We again transpose the matrix to make iteration easier
        transposed_matrix = self._reduced_matrix.transpose()

        for idx, now_row in enumerate(transposed_matrix):
            # Strawdummy values so we can fill our df in either case
            new_df_row = dict(birth=-1, death=-1, dimension=-1)
            new_df_row_barcode = dict(birth_value=-1, death_value=-1, dimension=-1)
            # assigning dimension
            new_df_row["dimension"] = self._boundary_matrix_dimens[idx]
            new_df_row_barcode["dimension"] = self._boundary_matrix_dimens[idx]
            if np.all((now_row == 0)):
                # assigning births
                new_df_row["birth"] = idx
                if self._distance_list:
                    new_df_row_barcode["birth_value"] = self._distance_list[idx]
                df_dictionary = pandas.DataFrame([new_df_row])
                df_dictionary_barcode = pandas.DataFrame([new_df_row_barcode])
                self._persistence_pairs = pandas.concat([self._persistence_pairs, df_dictionary])
                if self._distance_list:
                    self._reduced_matrix_barcode = pandas.concat([self._reduced_matrix_barcode, df_dictionary_barcode])
                continue
            # assigning deaths
            index_of_dying = np.where(transposed_matrix[idx] != 0)[0][-1]
            self._persistence_pairs.loc[self._persistence_pairs['birth'] == index_of_dying, "death"] = idx
            if self._distance_list:
                self._reduced_matrix_barcode.loc[self._persistence_pairs['birth'] == index_of_dying, "death_value"] = \
                    self._distance_list[idx]
        # assign infinity to the ones who are never closed
        self._persistence_pairs.loc[self._persistence_pairs['death'] == -1, "death"] = np.inf
        if self._distance_list:
            self._reduced_matrix_barcode.loc[self._reduced_matrix_barcode['death_value'] == -1, "death_value"] = np.inf

    def reduce_boundary_matrix(self):
        # print("Initial boundary matrix:")
        # print(self._bounday_matrix)
        # transpose rows with columns to iterate easier over the columns
        transposed_matrix = self._bounday_matrix.transpose()
        for index_of_current_row, _ in enumerate(transposed_matrix.copy()):
            # we made the function recursive
            transposed_matrix = reduction_of_column(transposed_matrix, index_of_current_row)
        final_matrix = transposed_matrix.transpose()
        # print("Reduced matrix:")
        # print(final_matrix)
        self._reduced_matrix = final_matrix
        self._calculate_persistence_pairs_and_barcode()

    def transform(self):
        raise NotImplementedError

    def predict(self):
        raise NotImplementedError

    def draw_persistence_diagram(self, plot_inf=False, title=None):
        print(self._reduced_matrix_barcode)
        assert type(self._reduced_matrix_barcode) == pandas.DataFrame
        df = self._reduced_matrix_barcode.copy()
        if plot_inf:
            max_value = df[df["death_value"] != np.inf]["death_value"].max() + 100
            df['death_value'].replace(np.inf, max_value, inplace=True)
        else:
            df = self._reduced_matrix_barcode.copy()
            df = df[df["death_value"] != np.inf]
            max_value = df[df["death_value"] != np.inf]["death_value"].max() + 1
        fig = px.scatter(df, x="birth_value", y="death_value", color="dimension")
        fig.update_layout(
            title=title if title else "Persistence Diagram",
            xaxis_range=[-1, max_value + 5],
            yaxis_range=[-1, max_value + 5],
            shapes=[
                {'type': 'line', 'yref': 'paper', 'xref': 'paper', 'y0': 0, 'y1': 1, 'x0': 0, 'x1': 1,
                 'layer': 'below'}])
        fig.show()


class PersistenceImages(object):
    """Persistence Images created by consuming a persistence bar code. For an example run, we refer to the method visualize_persistence_image()."""

    def __init__(self):
        self._size_of_each_pixel = 0.5  # Decides the resolution of the Discretized Kernel Density Distribution
        self._range_of_births = (0.0, 3)
        self._range_of_persistences = (0.0, 4)
        self._kernel_bandwidth = 1.0  # same default as sklearn
        self._width = self._range_of_births[1] - self._range_of_births[0]
        self._height = self._range_of_persistences[1] - self._range_of_persistences[0]
        self._number_of_samples_per_pixel = 10
        self._number_of_pixels = (
            int(self._width / self._size_of_each_pixel), int(self._height / self._size_of_each_pixel))

    def transform(self, persistence_barcode: pandas.DataFrame, is_in_birth_death_format=True, show_graphs=False):
        """ This method transforms a persistence barcode into a persistence image.
        :param persistence_barcode: The persistence barcode on which the persistence image is based on.
        :type persistence_barcode: pandas.DataFrame
        :param is_in_birth_death_format: Whether the persistence pairs is in (birth, death) tuple format
        :type is_in_birth_death_format: bool
        :param show_graphs: Whether we should show the graph visualization
        :type show_graphs: bool
        :return: The persistence image corressponding to the persistence diagram
        :rtype: np.array
        """
        """"""
        df = persistence_barcode.copy()
        max_value = df[df["death_value"] != np.inf]["death_value"].max()
        df['death_value'].replace(np.inf, max_value + 10, inplace=True)
        # convert from is_in_birth_death_format to birth persistence values
        df = df.to_numpy()
        if is_in_birth_death_format:
            df[:, 1] = df[:, 1] - df[:, 0]
        # changing out infinities
        # Construct meshgrid
        birth_density_interval = np.linspace(self._range_of_births[0], self._range_of_births[1],
                                             self._number_of_pixels[0] * self._number_of_samples_per_pixel)
        persistence_density_interval = np.linspace(self._range_of_persistences[0], self._range_of_persistences[1],
                                                   self._number_of_pixels[1] * self._number_of_samples_per_pixel)
        birth_discrete_interval = np.linspace(self._range_of_births[0], self._range_of_births[1],
                                              self._number_of_pixels[0])
        persistence_discrete_interval = np.linspace(self._range_of_persistences[0], self._range_of_persistences[1],
                                                    self._number_of_pixels[1])
        xx, yy = np.meshgrid(birth_density_interval, persistence_density_interval)
        xy = np.vstack([xx.ravel(), yy.ravel()]).T
        # creating the kernel density estimation
        kde = KernelDensity(kernel='gaussian', bandwidth=self._kernel_bandwidth).fit(df[:, 0:2])

        reshaping_tuple = (self._number_of_pixels[1] * self._number_of_samples_per_pixel,
                           self._number_of_pixels[0] * self._number_of_samples_per_pixel)
        density_values = np.exp(kde.score_samples(xy)).reshape(reshaping_tuple)

        conv_n = int(self._number_of_samples_per_pixel / self._size_of_each_pixel)
        kernel = np.ones((conv_n, conv_n))
        convolved = convolve2d(density_values, kernel, mode='valid')
        density_values_downsampled = convolved[::conv_n, ::conv_n] / conv_n
        persistence_image = density_values_downsampled
        if show_graphs:
            fig = make_subplots(rows=1, cols=2,
                                subplot_titles=('Kernel Density Distribution',
                                                f'Discretized Kernel Density Distribution:\n Pixel size: {self._size_of_each_pixel}x{self._size_of_each_pixel}'))

            fig.add_trace(go.Contour(
                z=density_values,
                line_smoothing=0,
                x=birth_density_interval,  # horizontal axis
                y=persistence_density_interval,  # vertical axis

            ), 1, 1)
            fig.add_trace(go.Contour(
                z=persistence_image,
                line_smoothing=0,
                x=birth_discrete_interval,  # horizontal axis
                y=persistence_discrete_interval,  # vertical axis
            ), 1, 2)
            fig.update_layout(title_text="Persistence Image on the two moons")
            fig.show()
        return persistence_image


class PersistenceLandscapes(object):
    """Persistence Landscapes. For an example run, we refer to the method visualize_persistence_landscape()."""

    def __init__(self, discretization_depth: int = 2):
        self._discretization_depth = discretization_depth

    def fit(self, persistence_barcode: pandas.DataFrame, show_graphs: bool = False):
        """This method transforms a persistence barcode into a persistence landscape.
        :param persistence_barcode: The persistence barcode on which the persistence landscape is based on.
        :type persistence_barcode: pandas.DataFrame
        :param show_graphs: Controls whether the result is displayed visually.
        :type show_graphs: bool
        :return: The matrix containing the unsorted landscape coordinates, and the matrix with sorted values
        :rtype: Tuple[pandas.DataFrame, pandas.DataFrame]
        """
        df = persistence_barcode.copy()
        # changing out infinities
        max_value = df[df["death_value"] != np.inf]["death_value"].max()
        df['death_value'].replace(np.inf, max_value + 10, inplace=True)
        df.loc[df.death_value == max_value + 10, "birth_value"] = max_value + 9

        df["half_life"] = np.divide(df["death_value"] - df["birth_value"], 2)
        df["mid_life"] = np.divide(df["death_value"] + df["birth_value"], 2)
        # creating coordinate system grid with linspace
        max_x = df["mid_life"].max()
        max_y = df["half_life"].max()
        x_range = np.linspace(0, int(max_x) + 1, int(self._discretization_depth * max_x))
        matrix = np.zeros([len(df), len(x_range)])
        for index, (_, series) in enumerate(df.iterrows()):
            current_value_row = np.copy(x_range)
            first_value = current_value_row - series.birth_value
            second_value = series.death_value - current_value_row
            final_row = np.min(np.array([first_value, second_value]), axis=0).clip(min=0)
            matrix[index, :] = final_row
        # Only for debugging
        # print(matrix)
        sorted_matrix = np.flip(matrix, axis=0)
        sorted_matrix = np.sort(sorted_matrix, axis=0)
        matrix_df = pandas.DataFrame(matrix.T)
        matrix_df.index = x_range
        sorted_matrix_df = pandas.DataFrame(sorted_matrix.T)
        sorted_matrix_df.index = x_range

        if show_graphs:

            fig = make_subplots(rows=2, cols=1,
                                subplot_titles=('Persistence landscape',
                                                'Persistence landscape sorted'))
            for i in range(len(matrix_df.columns)):
                fig.add_trace(go.Line(x=matrix_df[i].index.values, y=matrix_df[i].values,
                                      name=i,
                                      legendgroup="1",
                                      legendgrouptitle_text="The unsorted persistence landscape"),
                              row=1,
                              col=1)
                fig.add_trace(go.Line(x=sorted_matrix_df[i].index.values, y=sorted_matrix_df[i].values,
                                      name=f"k={i}",
                                      legendgroup="2",
                                      legendgrouptitle_text="The sorted persistence landscape"),
                              row=2,
                              col=1)
                fig.update_layout(title="Persistence Landscapes", title_font_size=20)
                fig.add_vline(x=max_value + 9, line_width=2, line_dash="dot", line_color="green",
                              annotation_text="never dying simplicies", annotation_position="bottom left",
                              annotation_font_size=12,
                              annotation_font_color="green")
            fig.show()

        return matrix_df, sorted_matrix_df


class PersLay(torch.nn.Module):
    """PersLay"""

    def __init__(self, layer_type="persistence_diagram", rho_output_dim_q=10, operation="sum"):
        super().__init__()
        self.operation = operation
        self.layer_type = layer_type
        if self.layer_type == "persistence_image":
            raise NotImplementedError
        elif self.layer_type == "persistence_landscape":
            raise NotImplementedError
        elif self.layer_type == "persistence_diagram":
            self.input_dimension = 2
            self.rho = torch.nn.Sequential(
                torch.nn.Linear(self.input_dimension, 124),
                torch.nn.ReLU(),
                torch.nn.Linear(124, 512),
                torch.nn.ReLU(),
                torch.nn.Linear(512, rho_output_dim_q),
                torch.nn.ReLU()
            )
            self.w = torch.nn.Sequential(
                torch.nn.Linear(self.input_dimension, 512),
                torch.nn.ReLU(),
                torch.nn.Linear(512, 256),
                torch.nn.ReLU(),
                torch.nn.Linear(256, 128),
                torch.nn.ReLU(),
                torch.nn.Linear(128, 1),
                torch.nn.ReLU()
            )
            self.final = torch.nn.Sequential(
                torch.nn.Linear(rho_output_dim_q, 4 * rho_output_dim_q),
                torch.nn.ReLU(),
                torch.nn.Linear(4 * rho_output_dim_q, rho_output_dim_q),
                torch.nn.ReLU(),
                torch.nn.Softmax(dim=0)
            )

    def forward(self, input_values):
        """Forward function of the perslay as neural network.
        :param input_values: Input vectors
        :type input_values: torch.Tensor
        :return: The output of this neural network
        :rtype: torch.Tensor
        """
        w_result = self.w(input_values)
        rho_result = self.rho(input_values)
        multiplication_result = torch.mul(w_result, rho_result)
        after_operation = self.permutation_invariant_operation(multiplication_result)
        after_softmax = self.final(after_operation)
        return after_softmax

    def permutation_invariant_operation(self, input_tensor: torch.Tensor):
        """Input tensors that can appear in different permutations each time are mixed together with a permutations invariant operation.
        :param input_tensor: Input tensors
        :type input_tensor: torch.Tensor
        :param operation: Three different permutation invariant operations are available: max, min, sum.
        :type operation: str
        :return: The input tensor reduced by one dimension
        :rtype: torch.Tensor
        """
        initial_tensor = input_tensor
        if self.operation is not None:
            if self.operation == "max":
                new_value, _ = torch.max(input_tensor, dim=0)
            elif self.operation == "min":
                new_value, _ = torch.min(input_tensor, dim=0)
            elif self.operation == "sum":
                new_value = torch.sum(input_tensor, dim=0)
            else:
                raise TypeError("operation should be max, min or sum")
            return new_value
        else:
            return initial_tensor


def visualize_matrix_reduction():
    """Tests the MatrixReduction class. Method is called visualize for conformity of style.
    :return: None
    :rtype: None
    """

    matrix_reductor = MatrixReduction(example_boundary_matrix, example_boundary_matrix_dimensions)
    matrix_reductor.reduce_boundary_matrix()
    reduced_matrix = matrix_reductor.get_reduced_matrix()
    df = matrix_reductor.get_persistence_pairs()
    assert np.array_equal(example_reduced_matrix, reduced_matrix)
    assert np.array_equal(df.sort_values(by="birth").to_numpy(),
                          example_persistence_pairs.sort_values(by="birth").to_numpy())
    print("Reduced Matrix has been correctly calculated! :)")


def visualize_filtered_complex():
    """Tests the FilteredComplexes class. Method is called visualize for conformity of style.
    :return: None
    :rtype: None
    """
    moon_coord, moon_label = make_moons(n_samples=10, noise=0.2, random_state=0)
    # Load and split data with a method from scikit-learn
    moon_train_coord, moon_test_coord, label_train, label_test = train_test_split(
        moon_coord, moon_label.astype(str), test_size=0.25, random_state=0)
    filtered_complex = FilteredComplexes(moon_train_coord)
    bounday_matrix, dimensional_array, dist_matrix = filtered_complex.fit(max_simplices_dim=4, k_nearest_neighours=3)
    print(bounday_matrix)
    print(dimensional_array)


def visualize_persistence_image():
    """Visualizes the results of the PersistenceImages class. We draw persistence image of the two moons
    :return: None
    :rtype: None
    """
    moon_coord, moon_label = make_moons(n_samples=10, noise=0.2, random_state=0)
    # Load and split data with a method from scikit-learn
    moon_train_coord, moon_test_coord, label_train, label_test = train_test_split(
        moon_coord, moon_label.astype(str), test_size=0.25, random_state=0)
    filtered_complex = FilteredComplexes(moon_train_coord)
    bounday_matrix, dimensional_array, dist_list = filtered_complex.fit(max_simplices_dim=4, k_nearest_neighours=3)
    matrix_reductor = MatrixReduction(bounday_matrix, dimensional_array, dist_list)
    matrix_reductor.reduce_boundary_matrix()
    persistence_barcode = matrix_reductor.get_barcode_of_reduced_matrix()
    persistent_image = PersistenceImages()
    persistent_image.transform(persistence_barcode=persistence_barcode, show_graphs=True)


def visualize_persistence_diagram():
    """Visualizes the results of the MatrixReduction class. We draw the persistence diagram of the two moons
    :return: None
    :rtype: None
    """
    moon_coord, moon_label = make_moons(n_samples=10, noise=0.2, random_state=0)
    # Load and split data with a method from scikit-learn
    moon_train_coord, moon_test_coord, label_train, label_test = train_test_split(
        moon_coord, moon_label.astype(str), test_size=0.25, random_state=0)
    filtered_complex = FilteredComplexes(moon_train_coord)
    bounday_matrix, dimensional_array, dist_list = filtered_complex.fit(max_simplices_dim=4, k_nearest_neighours=3)
    matrix_reductor = MatrixReduction(bounday_matrix, dimensional_array, dist_list)
    matrix_reductor.reduce_boundary_matrix()
    matrix_reductor.draw_persistence_diagram()


def visualize_persistence_landscape():
    """Visualizes the results of the PersistenceLandscapes class. We draw persistence landscape of the two moons
    :return: None
    :rtype: None
    """
    moon_coord, moon_label = make_moons(n_samples=10, noise=0.2, random_state=0)
    # Load and split data with a method from scikit-learn
    moon_train_coord, moon_test_coord, label_train, label_test = train_test_split(
        moon_coord, moon_label.astype(str), test_size=0.25, random_state=0)
    filtered_complex = FilteredComplexes(moon_train_coord)
    bounday_matrix, dimensional_array, dist_list = filtered_complex.fit(max_simplices_dim=4, k_nearest_neighours=3)
    matrix_reductor = MatrixReduction(bounday_matrix, dimensional_array, dist_list)
    matrix_reductor.reduce_boundary_matrix()
    persistent_landscapes = PersistenceLandscapes(discretization_depth=200)
    persistent_landscapes.fit(persistence_barcode=matrix_reductor.get_barcode_of_reduced_matrix(), show_graphs=True)


if __name__ == "__main__":
    visualize_filtered_complex()
    visualize_matrix_reduction()
    visualize_persistence_diagram()
    visualize_persistence_landscape()
    visualize_persistence_image()
