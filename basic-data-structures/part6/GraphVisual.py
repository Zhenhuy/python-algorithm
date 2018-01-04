#!/usr/bin/python
# -*- coding: UTF-8 -*-

import graphviz as gv
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import datetime

"""
可视化数据结构树
Author: wangdingqiao    http://blog.csdn.net/wangdingqiaoit
Date:2017-12-31
"""


class TreeVisualization(object):
    styles_config = {
        'graph': {
            'label': 'visualized by Wangdingqiao(Based on Graphviz)',
            'fontsize': '12',
            'fontcolor': 'blue',
            'bgcolor': '#FFFFFF',
            'rankdir': 'TB',
            'dpi': '1200',
            'labeljust': 'center',
            'labelloc': 'b',
            'nodesep': '0.35'
        },
        'nodes': {
            'shape': 'circle',
            'fontcolor': 'black',
            'fontsize': '12',
            'color': 'white',
            'style': 'filled',
            'fillcolor': '#006699',
            'fixedsize': 'true',
            'width': '0.8',
            'height': '0.4',
            'ordering': 'out'
        },
        'edges': {
            'style': 'bold',
            'color': 'blue',
            'arrowhead': 'normal',
            'fontsize': '6',
            'fontcolor': 'blue',
            'arrowsize': "0.6",
            'penwidth': "1"
        }
    }

    @staticmethod
    def apply_styles(graph, styles):
        graph.graph_attr.update(
            ('graph' in styles and styles['graph']) or {}
        )
        graph.node_attr.update(
            ('nodes' in styles and styles['nodes']) or {}
        )
        graph.edge_attr.update(
            ('edges' in styles and styles['edges']) or {}
        )
        return graph

    @staticmethod
    def show_tree(nodes, edges, file_name=None, view=False):
        if not file_name:
            file_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        g1 = gv.Digraph(format="jpg")
        for node_name, node_lab in nodes.items():
            if node_lab == 'NULL':
                g1.node(node_name, node_lab, style='invis')
            else:
                g1.node(node_name, node_lab)
        for edge_start, edge_end, is_visible in edges:
            if not is_visible:
                g1.edge(edge_start, edge_end, style='invis',  weight='100')
            else:
                g1.edge(edge_start, edge_end)
        TreeVisualization.apply_styles(g1, TreeVisualization.styles_config)
        g1.render(filename=file_name)
        if view:
            img = mpimg.imread(file_name+".jpg")
            plt.axis('off')
            plt.imshow(img)
            plt.show()


if __name__ == "__main__":
    nodes = {'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E': 'E', 'F': 'NULL', 'G': 'NULL'}
    edges = [('A', 'B', True), ('A', 'C', True), ('B', 'D', True), ('B', 'F', False), ('C', 'E', True), ('C', 'G', False)]
    TreeVisualization.show_tree(nodes, edges, None, True)
