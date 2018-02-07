#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
图的遍历算法 支持森林
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
    vertex_count = g.get_vertices_count()
    if not vertex_count:
        return
    un_visited_vertices = [i for i in range(vertex_count)]
    visited_vertices = []
    stack = []
    while un_visited_vertices:  # 当还有节点未访问到时 对于森林类型需要继续处理
        vertex = un_visited_vertices.pop(0)
        visited_vertices.append(vertex)
        stack.append(vertex)
        while stack:
            while stack:
                next_vertex = g.get_next_adjacent_vertex(stack[-1], visited_nodes=visited_vertices)
                if next_vertex == -1:
                    stack.pop(-1)
                else:
                    break
            if next_vertex != -1:
                visited_vertices.append(next_vertex)
                un_visited_vertices.remove(next_vertex)
                stack.append(next_vertex)
    print(visited_vertices)
    return visited_vertices


def breadth_first_traverse(g):
    """
    借助队列的广度优先遍历
    :return:遍历序列
    """
    vertex_count = g.get_vertices_count()
    if not vertex_count:
        return
    un_visited_vertices = [i for i in range(vertex_count)]
    queue = []
    visited_vertices = []
    while un_visited_vertices:
        vertex = un_visited_vertices.pop(0)
        queue.append(vertex)
        visited_vertices.append(vertex)
        while queue:
            front = queue.pop(0)
            while True:
                next_vertex = g.get_next_adjacent_vertex(front, visited_nodes=visited_vertices)
                if next_vertex == -1:
                    break
                visited_vertices.append(next_vertex)
                un_visited_vertices.remove(next_vertex)
                queue.append(next_vertex)
    return visited_vertices


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
    print('depth first traverse: ', [g.get_vertex_name(x) for x in depth_first_traverse(g)])
    print('breadth first traverse: ', [g.get_vertex_name(x) for x in breadth_first_traverse(g)])


def test_case_2():
    # 森林的类型
    vertex_to_name = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'P', 7: 'Q', 8: 'R', 9: 'X', 10: 'Y', 11: 'Z'}
    g = Graph(Graph.GRAPH_TYPE_UNDIRECTED, vertex_to_name, None)
    g.add_edges([Edge(0, 1), Edge(0, 3), Edge(1, 2), Edge(3, 4),
                 Edge(3, 5), Edge(6, 7), Edge(6, 8), Edge(9, 10), Edge(10, 11)])
    node_text_map, edges, directed = g.get_show_info()
    GraphVisualization.show(node_text_map, edges, is_directed=directed,
                            view_graph=True, rank_dir="LR", description="Forest")
    print('depth first traverse: ', [g.get_vertex_name(x) for x in depth_first_traverse(g)])
    print('breadth first traverse: ', [g.get_vertex_name(x) for x in breadth_first_traverse(g)])

if __name__ == "__main__":
    test_case_1()
