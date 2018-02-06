#!/usr/bin/python
# -*- coding: UTF-8 -*-
from graph import Graph
from graph import Edge
from GraphVisual import GraphVisualization

"""
拓扑排序 
reference-link

"""


def topological_sort_by_bfs(g):
    """
    拓扑排序 BFS实现
    :param g: 输入为有向无环图  directed acyclic graph (DAG)
    :return: 一个排序序列
    """
    if not g.is_directed_graph():
        raise AssertionError("only use to directed graph.")
    visited_order = []
    in_degree_zero_queue = []
    vertex_count = g.get_vertices_count()
    in_degrees = [0 for _ in range(vertex_count)]
    visited = [False for _ in range(vertex_count)]
    for vertex in range(vertex_count):
        in_degrees[vertex] = g.get_in_degree(vertex)
        if in_degrees[vertex] == 0:
            in_degree_zero_queue.append(vertex)
            visited[vertex] = True
    if not in_degree_zero_queue:
        raise AssertionError("Invalid graph for sort.")
    while in_degree_zero_queue:
        vertex_index = in_degree_zero_queue.pop(0)
        visited_order.append(vertex_index)
        for edge in g.get_adjacent_edges(vertex_index):  # BFS搜索相邻未访问过的定点
            if not visited[edge.to_vertex_index]:
                in_degrees[edge.to_vertex_index] -= 1
                if in_degrees[edge.to_vertex_index] == 0:
                    in_degree_zero_queue.append(edge.to_vertex_index)
                    visited[edge.to_vertex_index] = True
    for x in visited:
        if not x:
            raise AssertionError("invalid graph for topological sort, loop detected.")
    return visited_order


def test_case_1():
    vertex_to_name = {x: str(x+1) for x in range(5)}
    edge_list = [Edge(0, 1), Edge(0, 2), Edge(1, 2), Edge(1, 3), Edge(2, 3), Edge(2, 4)]
    g = Graph(Graph.GRAPH_TYPE_DIRECTED, vertex_to_name, edge_list)
    node_text_map, edges, directed = g.get_show_info()
    GraphVisualization.show(node_text_map, edges, is_directed=directed, view_graph=True, rank_dir="BT")
    visited_order = topological_sort_by_bfs(g)
    print('one topological sort of graph is:  ', [vertex_to_name[x] for x in visited_order])


def test_case_2():
    vertex_to_name = {x: str(x+1) for x in range(5)}
    # 存在环的有向图 (2, 3)-->(3, 4)-->(4, 2)
    edge_list = [Edge(0, 1), Edge(0, 2), Edge(1, 2), Edge(1, 3), Edge(2, 3), Edge(2, 4), Edge(3, 4), Edge(4, 2)]
    g = Graph(Graph.GRAPH_TYPE_DIRECTED, vertex_to_name, edge_list)
    node_text_map, edges, directed = g.get_show_info()
    GraphVisualization.show(node_text_map, edges, is_directed=directed, view_graph=True, rank_dir="BT")
    visited_order = topological_sort_by_bfs(g)
    print('one topological sort of graph is:  ', [vertex_to_name[x] for x in visited_order])

if __name__ == "__main__":
    test_case_1()