#import numpy as np
import pytest
import assignment_1.graph_processing as tp

def test_downstream_vertices():
    vertex_ids = [0, 2, 4]  # All unique vertex ids
    edge_ids = [1, 3]  # All unique edge ids
    edge_vertex_id_pairs = [(0, 2), (2, 4)]
    edge_enabled = [True, True]
    source_vertex_id = 0

    test3 = tp.GraphProcessor(
        vertex_ids=vertex_ids,
        edge_ids=edge_ids,
        edge_vertex_id_pairs=edge_vertex_id_pairs,
        edge_enabled=edge_enabled,
        source_vertex_id=source_vertex_id,
    )

    downstream_vertices = test3.find_downstream_vertices(1)
    assert downstream_vertices == [2, 4]

    downstream_vertices = test3.find_downstream_vertices(3)
    assert downstream_vertices == [4]
