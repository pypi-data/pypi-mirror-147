"""Reeb graph classes"""

import networkx as nx
import numpy as np
import plotly.graph_objects as go
from sklearn.cluster import DBSCAN
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split

from utils import draw_moons

# Filter functions
DISTANCE_TO_MEAN = "Distance to Mean"
PROJECTION = "Projection"
# Clustering methods
DBSCAN_METHOD = "DBSCAN"


class Mapper(object):
    """Mapper. For an example run, we refer to the method visualize_mapper()."""

    def __init__(self, filter_function: str = PROJECTION, number_of_intervals=7,
                 overlap_of_intervals_in_decimal_percent: float = 0.2,
                 clustering_function=DBSCAN_METHOD):
        self._graph = nx.Graph()
        self._filter_function = filter_function
        self._number_of_intervals = number_of_intervals
        self._overlap_of_intervals_in_decimal_percent = overlap_of_intervals_in_decimal_percent
        self._clustering_function = clustering_function
        self._node_number = 0

    def get_graph(self):
        """Getter function
        @return: Mapper
        @rtype: nx.Graph
        """
        return self._graph

    def get_next_node_number(self):
        """Getter function
        @return: current node number
        @rtype: int
        """
        self._node_number += 1
        return self._node_number - 1

    def fit(self, training_data):
        """Fits a mapper to the training data and saves the mapper as a nx.graph.
        :param training_data: Input training data
        :type training_data: np.array
        :return: None
        :rtype: None
        """
        yield self._graph
        # Get the whole image on R
        max_interval_border, min_interval_border = 0, 0
        image_values = 0
        if self._filter_function == DISTANCE_TO_MEAN:
            mean_value = np.mean(training_data, axis=0)
            euclidean_dist = np.array([np.linalg.norm(mean_value - sample) for sample in training_data])
            max_interval_border, min_interval_border = max(euclidean_dist), min(euclidean_dist)
            image_values = euclidean_dist
        elif self._filter_function == PROJECTION:
            # Works only for 2D data!!!!
            projection = np.array(training_data[:, 0])
            max_interval_border, min_interval_border = max(projection), min(projection)
            image_values = projection
        # Use the max and min value to set the interval borders
        interval_whole_length = max_interval_border - min_interval_border
        single_interval_length = np.divide(interval_whole_length, self._number_of_intervals)
        list_of_intervals = [
            {"lower": single_interval_length * interval_number + min_interval_border,
             "upper": single_interval_length * (interval_number + 1) + min_interval_border} for
            interval_number in range(self._number_of_intervals)]
        # Add overlap
        overlap = np.multiply(single_interval_length, self._overlap_of_intervals_in_decimal_percent)
        list_of_overlapping_intervals = [{"lower": dic["lower"] - overlap, "upper": dic["upper"] + overlap} for
                                         dic in list_of_intervals]
        print(list_of_overlapping_intervals)
        for idx, interval in enumerate(list_of_overlapping_intervals):
            # Find the values in the preimage which map to the given interval
            indexes_of_values_in_interval = np.where(
                (image_values < interval["upper"]) & (image_values > interval["lower"]))
            dbscan = DBSCAN(eps=0.25, min_samples=5)
            partial_training_data = training_data[indexes_of_values_in_interval]
            clustering = dbscan.fit(partial_training_data)
            print(clustering)
            print(dbscan.labels_)

            number_of_clusters = len(set(dbscan.labels_)) - (1 if -1 in dbscan.labels_ else 0)
            # Add as many nodes as there are clusters
            for label in range(number_of_clusters):
                # DBSCAN does not actually have a center for its clusters, but we want some nice visualizations
                center = np.mean(partial_training_data[dbscan.labels_ == label, :], axis=0)
                current_node_number = self.get_next_node_number()
                self._graph.add_node(current_node_number, interval_height=idx,
                                     cluster=partial_training_data[clustering.labels_ == label],
                                     vector=center)
                # Add an edge if the intersection between the the new cluster with the ones from the last interval
                # are not empty
                if idx is not 0:  # exclude first round
                    for node, attributes in self._graph.nodes(data=True):
                        if attributes["interval_height"] == (idx - 1):  # Nodes from last round
                            # Check if there are any intersections
                            set_new_cluster = set([tuple(x) for x in attributes["cluster"]])
                            set_old_cluster = set(
                                [tuple(x) for x in partial_training_data[clustering.labels_ == label]])
                            intersections = set_new_cluster.intersection(set_old_cluster)
                            if len(intersections) > 0:
                                self._graph.add_edge(node, current_node_number)

        yield self._graph

    def transform(self, sample):
        """Computes euclidean distance between the closest center in the
        Mapper graph representation and returns the corresponding label for the input sample.

        :param sample: The input sample
        :type sample: np.array
        :return: Label of closest center
        :rtype: int
        """
        min_value = 1000
        min_node = -1
        # Return the closest center
        for node, attributes in self._graph.nodes(data=True):
            norm_with_node = np.linalg.norm(attributes["vector"] - sample)
            if norm_with_node < min_value:
                min_value = norm_with_node
                min_node = node
        return min_node

    def predict(self):
        raise NotImplementedError


def visualize_mapper():
    """Visualization/Example of the Mapper on two moons data. Produces mapper_final.png as output.
    :return: None
    :rtype: None
    """
    moon_coord, moon_label = make_moons(n_samples=250, noise=0.02, random_state=0)
    # Load and split data with a method from scikit-learn
    moon_train_coord, moon_test_coord, label_train, label_test = train_test_split(
        moon_coord, moon_label.astype(str), test_size=0.25, random_state=0)
    filter_function = PROJECTION
    mapper = Mapper(filter_function=filter_function)
    results = list(mapper.fit(moon_train_coord))
    print(f"{len(results)} steps in total trained!")
    edge_x = []
    edge_y = []
    for edge in mapper.get_graph().edges():
        x0, y0 = mapper.get_graph().nodes[edge[0]]['vector'].flatten().tolist()
        x1, y1 = mapper.get_graph().nodes[edge[1]]['vector'].flatten().tolist()
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    node_x = []
    node_y = []
    for node in mapper.get_graph().nodes():
        x, y = mapper.get_graph().nodes[node]['vector'].flatten().tolist()
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
                title='Node Generation',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))
    node_generation = []
    node_text = []
    for node, attributes in mapper.get_graph().nodes(data=True):
        node_generation.append(attributes["interval_height"])
        node_text.append(f"Node height: {attributes['interval_height']}")

    node_trace.marker.color = node_generation
    node_trace.text = node_text
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title=f'Mapper on the two moons with {filter_function=} and DBSCAN clustering',
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
    fig.write_image("mapper_final.png", width=1400, height=1000)
    closest_center = mapper.transform(sample=moon_test_coord[0])
    print(f"Closest center to {moon_test_coord[0]} is node number: {closest_center}")


if __name__ == "__main__":
    visualize_mapper()
