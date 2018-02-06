#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
图的遍历算法
reference-link:
[1]-https://www.tutorialspoint.com/data_structures_algorithms/depth_first_traversal.htm
[2]-https://www.tutorialspoint.com/data_structures_algorithms/breadth_first_traversal.htm
"""

from graph import Graph
from graph import Edge
from GraphVisual import GraphVisualization


def depth_first_traverse(g):
    """
    借助栈的深度优先遍历
    :return: 遍历序列
    """
    if not g.get_vertices_count():
        return []
    visited_nodes = [0]
    stack = [0]
    while stack:
        while stack:
            next_node = g.get_next_adjacent_vertex(stack[-1], visited_nodes=visited_nodes)
            if next_node == -1:
                stack.pop(-1)
            else:
                break
        if next_node != -1:
            visited_nodes.append(next_node)
            stack.append(next_node)
    visited_order = []
    for x in visited_nodes:
        visited_order.append(g.get_vertex_name(x))
    return visited_order


def breadth_first_traverse(g):
    """
    借助队列的广度优先遍历
    :return:遍历序列
    """
    if not g.get_vertices_count():
        return []
    queue = [0]
    visited_nodes = [0]
    while queue:
        front = queue.pop(0)
        while True:
            next_node = g.get_next_adjacent_vertex(front, visited_nodes=visited_nodes)
            if next_node == -1:
                break
            visited_nodes.append(next_node)
            queue.append(next_node)
    visited_order = []
    for x in visited_nodes:
        visited_order.append(g.get_vertex_name(x))
    return visited_order


def test_case_1():
    vertex_to_name = {0: 'S', 1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G'}
    g = Graph(Graph.GRAPH_TYPE_UNDIRECTED, vertex_to_name, None)
    g.add_edge(Edge(0, 1))
    g.add_edge(Edge(0, 2))
    g.add_edge(Edge(0, 3))
    g.add_edge(Edge(1, 4))
    g.add_edge(Edge(2, 5))
    g.add_edge(Edge(3, 6))
    g.add_edge(Edge(4, 7))
    g.add_edge(Edge(5, 7))
    g.add_edge(Edge(6, 7))
    node_text_map, edges, directed = g.get_show_info()
    GraphVisualization.show(node_text_map, edges, is_directed=directed, view_graph=True, rank_dir="LR")
    print('depth first traverse: ', depth_first_traverse(g))
    print('breadth first traverse: ', breadth_first_traverse(g))


if __name__ == "__main__":
    test_case_1()
