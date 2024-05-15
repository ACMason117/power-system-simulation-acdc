import pytest  # Import pytest

import power_system_simulation.graph_processing as tp  # Import power_system_simpulation.graphy_processing


def test_alternative():
    vertex_ids = [0, 2, 4, 6, 10]  # All unique vertex ids
    edge_ids = [1, 3, 5, 7, 8, 9]  # All unique edge ids
    edge_vertex_id_pairs = [
        (0, 2),  # edge 1
        (0, 4),  # edge 3
        (0, 6),  # edge 5
        (2, 4),  # edge 7
        (4, 6),  # edge 8
        (2, 10),  # edge 9
    ]
    edge_enabled = [True, True, True, False, False, True]  # Whether each edge is enabled or disabled
    source_vertex_id = 0  # ID of the source vertex

    test2 = tp.GraphProcessor(
        vertex_ids=vertex_ids,
        edge_ids=edge_ids,
        edge_vertex_id_pairs=edge_vertex_id_pairs,
        edge_enabled=edge_enabled,
        source_vertex_id=source_vertex_id,
    )

    alternative_edges = test2.find_alternative_edges(1)  # Testcase 1 of find alternative edges
    assert alternative_edges == [7]

    alternative_edges = test2.find_alternative_edges(3)  # Testcase 2 of find alternative edges
    assert alternative_edges == [7, 8]

    alternative_edges = test2.find_alternative_edges(5)  # Testcase 3 of find alternative edges
    assert alternative_edges == [8]

    alternative_edges = test2.find_alternative_edges(9)  # Testcase 4 of find alternative edges
    assert alternative_edges == []


def test_downstream_vertices():
    vertex_ids = [0, 2, 4]  # All unique vertex ids
    edge_ids = [1, 3]  # All unique edge ids
    edge_vertex_id_pairs = [(0, 2), (2, 4)]  # Egde 1 and egde 3
    edge_enabled = [True, True]  # Whether each edge is enabled or disabled
    source_vertex_id = 0  # ID of the source vertex

    test3 = tp.GraphProcessor(
        vertex_ids=vertex_ids,
        edge_ids=edge_ids,
        edge_vertex_id_pairs=edge_vertex_id_pairs,
        edge_enabled=edge_enabled,
        source_vertex_id=source_vertex_id,
    )

    downstream_vertices = test3.find_downstream_vertices(1)  # Testcase 1 of find downstream vertices
    assert downstream_vertices == [2, 4]

    downstream_vertices = test3.find_downstream_vertices(3)  # Testcase 2 of find downstream vertices
    assert downstream_vertices == [4]
