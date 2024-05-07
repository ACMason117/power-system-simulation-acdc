import power_system_simulation.graph_processing as tp


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
    disabled_edge_id = 5

    test2 = tp.GraphProcessor(
        vertex_ids=vertex_ids,
        edge_ids=edge_ids,
        edge_vertex_id_pairs=edge_vertex_id_pairs,
        edge_enabled=edge_enabled,
        source_vertex_id=source_vertex_id,
    )

    alternative_edges = test2.find_alternative_edges(disabled_edge_id)
    assert alternative_edges == [8]
