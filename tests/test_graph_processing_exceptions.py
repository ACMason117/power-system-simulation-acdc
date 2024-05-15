import pytest

from assignment_1.graph_processing import (
    EdgePairNotUniqueError,
    GraphCycleError,
    GraphNotFullyConnectedError,
    GraphProcessor,
    IDNotFoundError,
    IDNotUniqueError,
    InputLengthDoesNotMatchError,
)


def test_id_vertex_not_unique():
    # tests the IDNotUniqueError for the unique vertex IDs
    with pytest.raises(IDNotUniqueError) as excinfo:
        GraphProcessor([1, 2, 3, 3, 5], [1, 2, 3], [(1, 2), (2, 3), (1, 5)], [True, True, True], 1)
    assert str(excinfo.value) == "Vertex IDs are not unique"


def test_id_edges_not_unique():
    # tests the IDNotUniqueError for the unique edge IDs
    with pytest.raises(IDNotUniqueError) as excinfo:
        GraphProcessor([1, 2, 3, 4, 5], [3, 1, 3, 2], [(1, 2), (2, 3), (1, 5), (4, 5)], [True, True, True, True], 1)
    assert str(excinfo.value) == "Edge IDs are not unique"


def test_longer_vertex_edge_pairs_list():
    # tests the InputLengthDoesNotMatchError when the vertex-edge pairs list is longer than the edge ID list
    with pytest.raises(InputLengthDoesNotMatchError) as excinfo:
        GraphProcessor([1, 2, 3, 4, 5], [3, 1], [(1, 2), (2, 3), (1, 5), (4, 5)], [True, True, True, True], 1)
    assert str(excinfo.value) == "Length of vertex-edge pairs list does not match edge ID list"


def test_longer_edge_id_list():
    # tests the InputLengthDoesNotMatchError when the vertex-edge pairs list is shorter than the edge ID list
    with pytest.raises(InputLengthDoesNotMatchError) as excinfo:
        GraphProcessor(
            [1, 2, 3, 4, 5], [3, 1, 4, 5, 6, 8], [(1, 2), (2, 3), (1, 5), (4, 5)], [True, True, True, True], 1
        )
    assert str(excinfo.value) == "Length of vertex-edge pairs list does not match edge ID list"


def test_ID_Not_Found_Error():
    # tests the IDNotFoundError for invalid edge ID in edge-vertex pair
    with pytest.raises(IDNotFoundError) as excinfo:
        GraphProcessor([1, 2, 3, 4, 5], [3, 1, 4, 5], [(1, 2), (2, 3), (1, 9), (4, 5)], [True, True, True, True], 1)
    assert str(excinfo.value) == "Edge-vertex ID pair contains non-valid vertex ID"

    with pytest.raises(IDNotFoundError) as excinfo:
        GraphProcessor([1, 2, 3, 4, 5], [3, 1, 4, 5], [(1, 2), (22, 3), (1, 5), (4, 5)], [True, True, True, True], 1)
    assert str(excinfo.value) == "Edge-vertex ID pair contains non-valid vertex ID"


def test_Edge_enabled_same_length():
    # tests the InputLengthDoesNotMatchError when the length of the edge enabled list does not match the length of the edge id list
    with pytest.raises(InputLengthDoesNotMatchError) as excinfo:
        GraphProcessor([1, 2, 3, 4], [3, 1, 4], [(1, 2), (2, 3), (1, 4)], [True, True], 1)
    assert str(excinfo.value) == "Length of enabled edge list does not match edge ID list"

    with pytest.raises(InputLengthDoesNotMatchError) as excinfo:
        GraphProcessor(
            [1, 2, 3, 4, 5], [3, 1, 4, 5], [(1, 2), (2, 3), (1, 4), (4, 5)], [True, True, True, True, True], 1
        )
    assert str(excinfo.value) == "Length of enabled edge list does not match edge ID list"

    with pytest.raises(InputLengthDoesNotMatchError) as excinfo:
        GraphProcessor(
            [1, 2, 3, 4, 5],
            [3, 1, 4, 5, 6],
            [(1, 2), (2, 3), (1, 4), (4, 5), (1, 5)],
            [
                True,
                True,
                False,
                True,
            ],
            1,
        )
    assert str(excinfo.value) == "Length of enabled edge list does not match edge ID list"


def test_source_vertex_ID_not_found():
    # tests the IDNotFoundError for when the source vertex ID is not found
    with pytest.raises(IDNotFoundError) as excinfo:
        GraphProcessor([1, 2, 3, 4, 5], [3, 1, 4, 5], [(1, 2), (2, 3), (1, 5), (4, 5)], [True, True, True, True], 8)
    assert str(excinfo.value) == "Source vertex ID is not a valid vertex ID"


def test_edge_pairs_not_unique_error():
    # tests the EdgePairNotUniqueError for when edge pairs are not unique
    with pytest.raises(EdgePairNotUniqueError) as excinfo:
        GraphProcessor(
            [1, 2, 3, 4, 5],
            [3, 1, 4, 5, 6],
            [(1, 2), (2, 3), (1, 5), (4, 5), (2, 3)],
            [True, True, True, True, True],
            1,
        )
    assert str(excinfo.value) == "Multiple edges connecting same 2 vertices found"
    with pytest.raises(EdgePairNotUniqueError) as excinfo:
        GraphProcessor(
            [1, 2, 3, 4, 5],
            [3, 1, 4, 5, 6],
            [(1, 2), (2, 3), (1, 5), (2, 1), (4, 5)],
            [True, True, True, True, True],
            1,
        )
    assert str(excinfo.value) == "Multiple edges connecting same 2 vertices found"
    with pytest.raises(EdgePairNotUniqueError) as excinfo:
        GraphProcessor(
            [1, 2, 3, 4, 5],
            [3, 1, 4, 5, 6],
            [(1, 2), (2, 3), (1, 5), (2, 1), (4, 5)],
            [True, True, True, False, True],
            1,
        )
    assert str(excinfo.value) == "Multiple edges connecting same 2 vertices found"


def test_graph_not_fully_connected_error():
    # tests the GraphNotFullyConnectedError for when the graph is not fully connected
    with pytest.raises(GraphNotFullyConnectedError) as excinfo:
        GraphProcessor([1, 2, 3, 4, 5], [3, 1, 4], [(1, 2), (2, 3), (1, 5)], [True, True, True], 1)
    assert str(excinfo.value) == "Graph not fully connected. Cannot reach all vertices."
    with pytest.raises(GraphNotFullyConnectedError) as excinfo:
        GraphProcessor([1, 2, 3, 4, 5], [3, 1, 4], [(1, 2), (2, 3), (4, 5)], [True, True, True], 1)
    assert str(excinfo.value) == "Graph not fully connected. Cannot reach all vertices."
    with pytest.raises(GraphNotFullyConnectedError) as excinfo:
        GraphProcessor([1, 2, 3, 4, 5], [3, 1, 4, 5], [(1, 2), (2, 3), (4, 5), (1, 5)], [True, True, True, False], 1)
    assert str(excinfo.value) == "Graph not fully connected. Cannot reach all vertices."


def test_cycle_error():
    # tests the GraphCycleError for when there are cycles
    with pytest.raises(GraphCycleError) as excinfo:
        GraphProcessor(
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [(1, 2), (2, 3), (3, 4), (2, 5), (5, 6), (5, 7), (7, 8), (6, 7), (6, 8)],
            [True, True, True, True, True, True, True, True, True],
            1,
        )
    assert str(excinfo.value) == "Cycle found"
    with pytest.raises(GraphCycleError) as excinfo:
        GraphProcessor(
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [(1, 2), (2, 3), (3, 4), (2, 5), (5, 6), (5, 7), (7, 8), (6, 3)],
            [True, True, True, True, True, True, True, True],
            1,
        )
    assert str(excinfo.value) == "Cycle found"
    with pytest.raises(GraphCycleError) as excinfo:
        GraphProcessor(
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [(1, 2), (2, 3), (3, 4), (6, 3), (2, 5), (5, 6), (5, 7), (7, 8)],
            [True, True, True, True, True, True, True, False],
            1,
        )
    assert str(excinfo.value) == "Cycle found"
    with pytest.raises(GraphCycleError) as excinfo:
        GraphProcessor(
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [(1, 2), (2, 3), (3, 4), (2, 5), (5, 6), (5, 7), (7, 8), (6, 3), (1, 7)],
            [True, True, True, True, True, True, True, True, True],
            1,
        )
    assert str(excinfo.value) == "Cycle found"
    with pytest.raises(GraphCycleError) as excinfo:
        GraphProcessor(
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [(6, 2), (1, 2), (2, 3), (3, 4), (2, 5), (5, 6), (5, 7), (7, 8)],
            [True, True, True, True, True, True, True, True],
            5,
        )
    assert str(excinfo.value) == "Cycle found"
