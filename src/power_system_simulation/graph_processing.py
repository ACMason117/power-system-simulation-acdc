"""
This is a skeleton for the graph processing assignment.

We define a graph processor class with some function skeletons. Test
"""

from enum import IntEnum
from typing import List, Tuple

import networkx as nx


class EnabledEdges(IntEnum):
    """Criterium for plotting: Only enabled edges"""


class AllEdges(IntEnum):
    """Criterium for plotting: All edges"""


class IDNotFoundError(Exception):
    """Raises IDNotFoundError if vertex or edge ID is not found

    Args:
        Exception: _description_
    """


class InputLengthDoesNotMatchError(Exception):
    """Raises InputLengthDoesNotMatchError if number of enabled edges is not equal to number of edge IDs

    Args:
        Exception: _description_
    """


class IDNotUniqueError(Exception):
    """Raises IDNotUniqueError if duplicate vertex or edge ID is found

    Args:
        Exception: _description_
    """


class EdgePairNotUniqueError(Exception):
    """Raises EdgePairNotUniqueError if multiple edge connects the same vertices

    Args:
        Exception: _description_
    """


class GraphNotFullyConnectedError(Exception):
    """Raises GraphNotFullyConnectedError if any vertex in the graph is unreachable

    Args:
        Exception: _description_
    """


class GraphCycleError(Exception):
    """Raises GraphCycleError if any cycles in the graph are found

    Args:
        Exception: _description_
    """


class EdgeAlreadyDisabledError(Exception):
    """Raises EdgeAlreadyDisabledError if find_alternative_edge function tries to disable
        an edge that is already disabled

    Args:
        Exception: _description_
    """


class GraphProcessor:
    """
    General documentation of this class.
    You need to describe the purpose of this class and the functions in it.
    We are using an undirected graph in the processor.
    """

    # add parent list, adjacency list and potentially more
    def __init__(
        self,
        vertex_ids: List[int],
        edge_ids: List[int],
        edge_vertex_id_pairs: List[Tuple[int, int]],
        edge_enabled: List[bool],
        source_vertex_id: int,
    ) -> None:
        """
        Initialize a graph processor object with an undirected graph.
        Only the edges which are enabled are taken into account.
        Check if the input is valid and raise exceptions if not.
        The following conditions should be checked:
            1. vertex_ids and edge_ids should be unique. (IDNotUniqueError)
            2. edge_vertex_id_pairs should have the same length as edge_ids. (InputLengthDoesNotMatchError)
            3. edge_vertex_id_pairs should contain valid vertex ids. (IDNotFoundError)
            4. edge_enabled should have the same length as edge_ids. (InputLengthDoesNotMatchError)
            5. source_vertex_id should be a valid vertex id. (IDNotFoundError)
            6. The graph should be fully connected. (GraphNotFullyConnectedError)
            7. The graph should not contain cycles. (GraphCycleError)
        If one certain condition is not satisfied, the error in the parentheses should be raised.

        Args:
            vertex_ids: list of vertex ids
            edge_ids: list of edge ids
            edge_vertex_id_pairs: list of tuples of two integer
                Each tuple is a vertex id pair of the edge.
            edge_enabled: list of bools indicating of an edge is enabled or not
            source_vertex_id: vertex id of the source in the graph
        """
        self.vertex_ids = vertex_ids
        self.edge_ids = edge_ids
        self.edge_vertex_id_pairs = edge_vertex_id_pairs
        self.edge_enabled = edge_enabled
        self.source_vertex_id = source_vertex_id

        # 1. vertex_ids and edge_ids should be unique
        if len(set(vertex_ids)) != len(vertex_ids):
            raise IDNotUniqueError("Vertex IDs are not unique")
        if len(set(edge_ids)) != len(edge_ids):
            raise IDNotUniqueError("Edge IDs are not unique")

        # 2. edge_vertex_id_pairs should have the same length as edge_ids
        if len(edge_vertex_id_pairs) != len(edge_ids):
            raise InputLengthDoesNotMatchError("Length of vertex-edge pairs list does not match edge ID list")

        # 3. edge_vertex_id_pairs should contain valid vertex ids
        for i in range(len(edge_ids)):
            vertex1, vertex2 = edge_vertex_id_pairs[i]

            if vertex1 not in vertex_ids or vertex2 not in vertex_ids:
                raise IDNotFoundError("Edge-vertex ID pair contains non-valid vertex ID")

        # 4. edge_enabled should have the same length as edge_ids
        if len(edge_enabled) != len(edge_ids):
            raise InputLengthDoesNotMatchError("Length of enabled edge list does not match edge ID list")

        # 5. source_vertex_id should be a valid vertex id
        if source_vertex_id not in vertex_ids:
            raise IDNotFoundError("Source vertex ID is not a valid vertex ID")

        # custom Errors
        if len(edge_vertex_id_pairs) != len(set(sort_tuple_list(edge_vertex_id_pairs))):
            raise EdgePairNotUniqueError("Multiple edges connecting same 2 vertices found")

        # 6. The graph should not contain cycles (checked inside dfs)
        vertex_visited = []
        vertex_parents = {}
        adjacency_list = self.build_adjacency_list(edge_vertex_id_pairs, edge_enabled)
        if self.dfs(adjacency_list, vertex_visited, float("Nan"), vertex_parents, source_vertex_id) == 1:
            raise GraphCycleError("Cycle found")

        # 7. The graph should be fully connected
        if len(vertex_visited) != len(vertex_ids):
            raise GraphNotFullyConnectedError("Graph not fully connected. Cannot reach all vertices.")

    def dfs(self, adjacency_list, visited, parent, parent_list, start_node) -> List[int]:
        """
        Given an GraphProcessor, return Depth First Search visited nodes list and parent list.
        """

        # start dfs from start_node
        if start_node not in visited:  # check if node has been visited
            visited.append(start_node)
            parent_list[start_node] = parent  # assign parent of node

            for adjacent_vertex in adjacency_list[start_node]:
                if adjacent_vertex != parent:
                    if adjacent_vertex in visited:
                        # Cycle detected, return 1
                        return 1
                    if self.dfs(adjacency_list, visited, start_node, parent_list, adjacent_vertex) == 1:
                        return 1

        # If no cycle is found
        return 0

    def build_adjacency_list(self, edge_vertex_id_pairs, edge_enabled):
        """Given a GraphProcessor, return an undirected adjacency list using only enabled edges.

        Args:
            edge_vertex_id_pairs: List[Tuple[int, int]]
            edge_enabled: List[Bool]

        Returns:
            dict
        """

        adjacency_list = {}
        enabled_edges = [num for num, m in zip(edge_vertex_id_pairs, edge_enabled) if m]

        for edge in enabled_edges:  # cycle through edge IDs
            u, v = edge  # tuple unpacking

            if u not in adjacency_list:  # check if list for vertex u exists
                adjacency_list[u] = []
            if v not in adjacency_list:  # check if list for vertex u exists
                adjacency_list[v] = []

            adjacency_list[u].append(v)
            adjacency_list[v].append(u)

        return adjacency_list

    def find_downstream_vertices(self, edge_id: int) -> List[int]:
        """
        Given an edge id, return all the vertices which are in the downstream of the edge,
            with respect to the source vertex.
            Including the downstream vertex of the edge itself!

        Only enabled edges should be taken into account in the analysis.
        If the given edge_id is a disabled edge, it should return empty list.
        If the given edge_id does not exist, it should raise IDNotFoundError.


        For example, given the following graph (all edges enabled):

            vertex_0 (source) --edge_1-- vertex_2 --edge_3-- vertex_4

        Call find_downstream_vertices with edge_id=1 will return [2, 4]
        Call find_downstream_vertices with edge_id=3 will return [4]

        Args:
            edge_id: edge id to be searched

        Returns:
            A list of all downstream vertices.
        """
        if edge_id not in self.edge_ids:
            raise IDNotFoundError("Edge ID not found in graph.")

        # step 1: run dfs to build parent list
        vertex_visited = []
        vertex_parents = {}
        adjacency_list = self.build_adjacency_list(self.edge_vertex_id_pairs, self.edge_enabled)
        self.dfs(
            adjacency_list, vertex_visited, float("Nan"), vertex_parents, self.source_vertex_id
        )  # cannot be cyclic, don't check

        # step 2: receive disabled edge
        index_disabled_edge = self.edge_ids.index(edge_id)
        disabled_edge = self.edge_vertex_id_pairs[index_disabled_edge]

        # step 3: choose new start point (child)
        if disabled_edge[0] == vertex_parents[disabled_edge[1]]:
            # if first vertex in edge is parent of second vertex, pick second (child) vertex
            downstream_vertex_source = disabled_edge[1]
        else:
            # otherwise first vertex must be the child
            downstream_vertex_source = disabled_edge[0]

        # step 4: set disabled edge to false
        self.edge_enabled[index_disabled_edge] = False

        # step 5: run dfs from new source vertex id
        vertex_downstream_visited = []
        vertex_downstream_parents = {}
        adjacency_downstream_list = self.build_adjacency_list(self.edge_vertex_id_pairs, self.edge_enabled)

        if downstream_vertex_source not in adjacency_downstream_list:
            vertex_downstream_visited.append(downstream_vertex_source)
        else:
            self.dfs(
                adjacency_downstream_list,
                vertex_downstream_visited,
                float("Nan"),
                vertex_downstream_parents,
                downstream_vertex_source,
            )

        # step 6: set disabled edge back to true
        self.edge_enabled[index_disabled_edge] = True

        return vertex_downstream_visited

    def find_alternative_edges(self, disabled_edge_id: int) -> List[int]:
        """
        Given an enabled edge, do the following analysis:
            If the edge is going to be disabled,
                which (currently disabled) edge can be enabled to ensure
                that the graph is again fully connected and acyclic?
            Return a list of all alternative edges.
        If the disabled_edge_id is not a valid edge id, it should raise IDNotFoundError.
        If the disabled_edge_id is already disabled, it should raise EdgeAlreadyDisabledError.
        If there are no alternative to make the graph fully connected again, it should return empty list.


        For example, given the following graph:

        vertex_0 (source) --edge_1(enabled)-- vertex_2 --edge_9(enabled)-- vertex_10
                 |                               |
                 |                           edge_7(disabled)
                 |                               |
                 -----------edge_3(enabled)-- vertex_4
                 |                               |
                 |                           edge_8(disabled)
                 |                               |
                 -----------edge_5(enabled)-- vertex_6

        Call find_alternative_edges with disabled_edge_id=1 will return [7]
        Call find_alternative_edges with disabled_edge_id=3 will return [7, 8]
        Call find_alternative_edges with disabled_edge_id=5 will return [8]
        Call find_alternative_edges with disabled_edge_id=9 will return []

        Args:
            disabled_edge_id: edge id (which is currently enabled) to be disabled

        Returns:
            A list of alternative edge ids.
        """
        # Step 1: Check if the disabled_edge_id is valid
        if disabled_edge_id not in self.edge_ids:
            raise IDNotFoundError("Edge ID not found.")

        # Step 2: Check if the edge corresponding to disabled_edge_id is currently enabled
        edge_index = self.edge_ids.index(disabled_edge_id)
        if not self.edge_enabled[edge_index]:
            raise EdgeAlreadyDisabledError("Edge is already disabled.")

        self.edge_enabled[edge_index] = False
        # List to store alternative edge ids
        alternative_edges = []

        # Step 3: Iterate through each disabled edge, check if enabling makes the graph fully connected and acyclic
        for i, edge_enabled in enumerate(self.edge_enabled):
            if not edge_enabled:  # Check only disabled edges
                if self.edge_ids[i] != disabled_edge_id:
                    # Step 4: Enable the disabled edge temporarily
                    self.edge_enabled[i] = True

                    # Step 5: Build adjacency list
                    enabled_edge_vertex_id_pairs = []
                    edge_enabled_short = []
                    for j in range(len(self.edge_ids)):
                        if self.edge_enabled[j]:
                            enabled_edge_vertex_id_pairs.append(self.edge_vertex_id_pairs[j])
                            edge_enabled_short.append(self.edge_enabled[j])
                            continue

                    adjacency_list = self.build_adjacency_list(enabled_edge_vertex_id_pairs, edge_enabled_short)

                    # Perform Depth First Search (dfs) to check for cycles
                    visited = []
                    parent_list = {}

                    if self.dfs(adjacency_list, visited, None, parent_list, self.source_vertex_id) == 1:
                        # If a cycle is detected, revert the edge back to disabled and continue to the next edge
                        self.edge_enabled[i] = False
                    elif self.dfs(adjacency_list, visited, None, parent_list, self.source_vertex_id) == 0:
                        # Step 6: If enabling a disabled edge satisfies the conditions,
                        # add its edge id to the list of alternatives
                        if len(visited) == len(self.vertex_ids):
                            alternative_edges.append(self.edge_ids[i])
                            self.edge_enabled[i] = False
                        # Revert the edge back to disabled
                        self.edge_enabled[i] = False

        # Revert input edge back to enabled
        self.edge_enabled[edge_index] = True

        # Return alternative edges list
        return alternative_edges

    def graph_plotter(self, plot_criteria=EnabledEdges) -> None:
        """Prints GraphProcessor using NetworkX.

        Returns:
            _description_
        """
        graph = nx.Graph()
        graph.add_nodes_from(self.vertex_ids)
        if plot_criteria == EnabledEdges:
            enabled_edges = [num for num, m in zip(self.edge_vertex_id_pairs, self.edge_enabled) if m]
            graph.add_edges_from(enabled_edges)
        elif plot_criteria == AllEdges:
            graph.add_edges_from(self.edge_vertex_id_pairs)

        nx.draw(graph, with_labels=True)


# other functions not dependent on specific class


def sort_tuple_list(edge_vertex_id_pairs) -> List[Tuple[int, int]]:
    """Sorts the edge_vertex_id_pairs tuple list of GraphProcessor class.
    Args:
        edge_vertex_id_pairs: List[Tuple[int, int]]

    Returns:
        List[Tuple[int, int]]
    """

    # sort each tuple in ascending order
    sorted_tuple_list = [tuple(sorted(t)) for t in edge_vertex_id_pairs]

    # sort each tuple based on initial value
    sorted_tuple_list = sorted(sorted_tuple_list, key=lambda x: x[0])

    return sorted_tuple_list
