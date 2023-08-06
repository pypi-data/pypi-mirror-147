import plotly.graph_objects as go


def draw_moons(fig, moon_train_coord, moon_test_coord, label_train, label_test):
    """Draws the two moons from Sklearn.
    :param fig: Incoming plotly figure
    :type fig: plotly.figure
    :param moon_train_coord: Coordinates of the training data for the two moons
    :type moon_train_coord: np.array
    :param moon_test_coord: Coordinates of the test data for the two moons
    :type moon_test_coord: np.array
    :param label_train: Labels of the training data for the two moons
    :type label_train: np.array
    :param label_test: Labels of the test data for the two moons
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
