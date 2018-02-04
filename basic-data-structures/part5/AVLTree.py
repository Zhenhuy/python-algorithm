#!/usr/bin/python
# -*- coding: UTF-8 -*-
import GraphVisual
from binarySearchTree import BinarySearchTree
import random

"""
AVL Tree
reference link:
1-https://cs.gmu.edu/~setia/cs310/slides/avl.pdf
2-http://kabulcs.weebly.com/uploads/5/0/3/5/5035021/chapter_8_-_avl_trees.pdf
"""


class AVLTreeNode(object):
    """
    树节点
    """
    LEFT_HIGHER = -1
    EQUAL_HEIGHT = 0
    RIGHT_HIGHER = 1

    def __init__(self, data, left=None, right=None, parent=None, bf=0):
        self.data = data
        self.left, self.right = left, right
        self.parent = parent
        self.bf = bf

    def __str__(self):
        return str(self.data) + "bf(" + str(self.bf) + ")"

    def __repr__(self):
        return self.__str__()


class BoolObject(object):
    """
    可变布尔对象
    """
    def __init__(self, status=False):
        self.status = status

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status

    def __str__(self):
        return (self.status and 'True') or 'False'

    def __repr__(self):
        return self.__str__()


class AVLTree(BinarySearchTree):
    """
        AVL Tree 自平衡的二叉搜索树
    """

    def __init__(self):
        self.root = None

    def __init__(self, data_array):
        if type(data_array) is not list:
            raise ValueError('init with data array only')
        self.root = None
        for x in data_array:
            self.add(x)

    def add(self, value):
        if not self.root:
            self.root = AVLTreeNode(value)
            return True
        else:
            return self.__add_value__(self.root, value, BoolObject(False))

    def __add_value__(self, node, value, taller):
        result = True
        if not node:
            result = False
        elif node.data == value:
            result = False       # duplicate
        elif value < node.data:
            if node.left:
                result = self.__add_value__(node.left, value, taller)
            else:
                node.left = AVLTreeNode(value, parent=node)
                taller.set_status(True)
            if result and taller.get_status():
                if node.bf == AVLTreeNode.LEFT_HIGHER:  # 在左子树插入前已经左边高则需要平衡处理
                    self.left_balance(node)
                    taller.set_status(False)
                elif node.bf == AVLTreeNode.EQUAL_HEIGHT:  # 在左子树插入前节点平衡则现在左边变高
                    node.bf = AVLTreeNode.LEFT_HIGHER
                else:
                    node.bf = AVLTreeNode.EQUAL_HEIGHT  # 在左子树插入前节点右边高则现在平衡了
                    taller.set_status(False)
        else:
            if node.right:
                result = self.__add_value__(node.right, value, taller)
            else:
                node.right = AVLTreeNode(value, parent=node)
                taller.set_status(True)
            if result and taller.get_status():
                if node.bf == AVLTreeNode.LEFT_HIGHER:  # 插入右子树前节点左边高则现在平衡了
                    node.bf = AVLTreeNode.EQUAL_HEIGHT
                    taller.set_status(False)
                elif node.bf == AVLTreeNode.EQUAL_HEIGHT:  # 插入右子树前节点平衡则现在右边高了
                    node.bf = AVLTreeNode.RIGHT_HIGHER
                else:  # 插入右子树前节点已经右边高了则需要平衡处理
                    self.right_balance(node)
                    taller.set_status(False)
        return result

    def remove_by_recursion(self, value):
        return self.__remove__(self.root, value, BoolObject(False))

    def __remove__(self, node, value, shorter):
        result = False
        if not node:
            return False
        is_remove_at_right = False
        if value == node.data:
            if node.left and node.right:  # case 被删除节点左右孩子都存在
                min_node = node.right
                while min_node.left:
                    min_node = min_node.left
                node.data = min_node.data
                is_remove_at_right = True
                result = self.__remove__(node.right, node.data, shorter)
            else:                        # case 最多只有一个孩子存在
                if node.parent:
                    if node == node.parent.left:
                        node.parent.left = node.left or node.right
                        if node.parent.left:
                            node.parent.left.parent = node.parent
                    else:
                        node.parent.right = node.left or node.right
                        if node.parent.right:
                            node.parent.right.parent = node.parent
                    shorter.set_status(True)
                else:
                    self.root = node.left or node.right
                    if self.root:
                        self.root.parent = None
                    shorter.set_status(False)
                return True
        elif value < node.data and node.left:
            result = self.__remove__(node.left, value, shorter)
        elif value > node.data and node.right:
            is_remove_at_right = True
            result = self.__remove__(node.right, value, shorter)
        if result and shorter.get_status():
            self.remove_balance(node, is_remove_at_right, shorter)
        return result

    def remove_balance(self, node, is_remove_at_right, shorter):
        if not node:
            raise AssertionError('remove_balance to empty node.')
        if node.bf == AVLTreeNode.EQUAL_HEIGHT:  # case 1 节点删除之前已经平衡 则调整平衡因子 树高度不变
            node.bf = (is_remove_at_right and AVLTreeNode.LEFT_HIGHER) or AVLTreeNode.RIGHT_HIGHER
            shorter.set_status(False)
            print('remove balance case 1', node, shorter)
        elif (node.bf == AVLTreeNode.LEFT_HIGHER and not is_remove_at_right) \
                or (node.bf == AVLTreeNode.RIGHT_HIGHER and is_remove_at_right):  # case 2 节点删除之前不平衡在较高子树删除
            node.bf = AVLTreeNode.EQUAL_HEIGHT
            shorter.set_status(True)
            print('remove balance case 2', node, shorter)
        else:  # case 3 节点删除之前不平衡 在较低子树删除节点后需要平衡处理
            if node.bf == AVLTreeNode.LEFT_HIGHER:
                left_node = node.left  # 较高子树根
                if left_node.bf == AVLTreeNode.EQUAL_HEIGHT:  # case 3a 较高子树根节点平衡
                    self.right_rotate(node)
                    left_node.bf = AVLTreeNode.RIGHT_HIGHER
                    shorter.set_status(False)
                    print('remove balance case 3a left', node, shorter)
                elif left_node.bf == AVLTreeNode.LEFT_HIGHER:  # case 3b 较高子树根节点和node平衡因子一样
                    self.right_rotate(node)
                    node.bf = AVLTreeNode.EQUAL_HEIGHT
                    left_node.bf = AVLTreeNode.EQUAL_HEIGHT
                    shorter.set_status(True)
                    print('remove balance case 3b left', node)
                else:  # case 3c 较高子树根节点和node平衡因子相反
                    self.left_balance(node)
                    shorter.set_status(True)
                    print('remove balance case 3c left', node, shorter)
            elif node.bf == AVLTreeNode.RIGHT_HIGHER:
                right_child = node.right
                if right_child.bf == AVLTreeNode.EQUAL_HEIGHT:
                    self.left_rotate(node)
                    right_child.bf = AVLTreeNode.LEFT_HIGHER
                    shorter.set_status(False)
                    print('remove balance case 3a right', node, shorter)
                elif right_child.bf == AVLTreeNode.RIGHT_HIGHER:
                    self.left_rotate(node)
                    node.bf = AVLTreeNode.EQUAL_HEIGHT
                    right_child.bf = AVLTreeNode.EQUAL_HEIGHT
                    print('remove balance case 3b right', node, shorter)
                else:
                    self.right_balance(node)
                    shorter.set_status(True)
                    print('remove balance case 3c right', node, shorter)

    def left_balance(self, node):
        """
        左平衡处理
        :param node: 待处理节点
        :return: None
        """
        if not node or not node.left:
            raise AssertionError(" left balance to illegal node " + str(node))
        left_node = node.left
        if left_node.bf == AVLTreeNode.LEFT_HIGHER:   # LL型 右旋转
            node.bf = AVLTreeNode.EQUAL_HEIGHT
            left_node.bf = AVLTreeNode.EQUAL_HEIGHT
            self.right_rotate(node)
        elif left_node.bf == AVLTreeNode.RIGHT_HIGHER:    # LR型 先左旋转 后右旋转
            left_node_right = left_node.right
            if left_node_right.bf == AVLTreeNode.LEFT_HIGHER:
                node.bf = AVLTreeNode.RIGHT_HIGHER
                left_node.bf = AVLTreeNode.EQUAL_HEIGHT
            elif left_node_right.bf == AVLTreeNode.RIGHT_HIGHER:
                node.bf = AVLTreeNode.EQUAL_HEIGHT
                left_node.bf = AVLTreeNode.LEFT_HIGHER
            else:
                node.bf = AVLTreeNode.EQUAL_HEIGHT
                left_node.bf = AVLTreeNode.EQUAL_HEIGHT
            left_node_right.bf = AVLTreeNode.EQUAL_HEIGHT
            self.left_rotate(left_node)
            self.right_rotate(node)
        else:
            raise AssertionError(" logic error , should not left balance node " + str(node))

    def right_balance(self, node):
        if not node or not node.right:
            raise AssertionError(" right balance to illegal node " + str(node))
        node_right = node.right
        if node_right.bf == AVLTreeNode.RIGHT_HIGHER:  # RR型 左旋转
            node.bf = AVLTreeNode.EQUAL_HEIGHT
            node_right.bf = AVLTreeNode.EQUAL_HEIGHT
            self.left_rotate(node)
        elif node.right.bf == AVLTreeNode.LEFT_HIGHER:  # RL型 先右旋转后左旋转
            node_right_left = node_right.left
            if node_right_left.bf == AVLTreeNode.LEFT_HIGHER:
                node.bf = AVLTreeNode.EQUAL_HEIGHT
                node_right.bf = AVLTreeNode.RIGHT_HIGHER
            elif node_right_left.bf == AVLTreeNode.RIGHT_HIGHER:
                node.bf = AVLTreeNode.LEFT_HIGHER
                node_right.bf = AVLTreeNode.EQUAL_HEIGHT
            else:
                node.bf = AVLTreeNode.EQUAL_HEIGHT
                node_right.bf = AVLTreeNode.EQUAL_HEIGHT
            node_right_left.bf = AVLTreeNode.EQUAL_HEIGHT
            self.right_rotate(node_right)
            self.left_rotate(node)
        else:
            raise AssertionError(" logic error , should not right balance node " + str(node))

    def left_rotate(self, node):
        """
        左旋转调整节点node
             p							q
           /  \ 					   / \
          s    q			=> 	  	  p  qr
              / \					/  \
             ql  qr			       s   ql
        :param node: 待调整节点
        :return: None
        """
        if not node or not node.right:
            raise AssertionError(" left rotate to illegal node " + str(node))
        parent_node = node.parent
        node_right = node.right
        node.right = node_right.left
        if node.right:
            node.right.parent = node
        node_right.left = node
        node.parent = node_right
        if parent_node:
            if node == parent_node.left:
                parent_node.left = node_right
            else:
                parent_node.right = node_right
            node_right.parent = parent_node
        else:
            self.root = node_right
            node_right.parent = None
        print('left rotate ', node)

    def right_rotate(self, node):
        """
        右旋转调整节点node
            p						 q
           / \					   /  \
          q   s		=>  	      ql   p
         /  \						  / \
        ql  qr  					 qr  s
        :param node: 待调整节点
        :return: None
        """
        if not node or not node.left:
            raise AssertionError(" right rotate to illegal node " + str(node))
        parent_node = node.parent
        node_left = node.left
        node.left = node_left.right
        if node.left:
            node.left.parent = node
        node_left.right = node
        node.parent = node_left
        if parent_node:
            if node == parent_node.left:
                parent_node.left = node_left
            else:
                parent_node.right = node_left
            node_left.parent = parent_node
        else:
            self.root = node_left
            node_left.parent = None
        print('right rotate ', node)

    def left_right_rotate(self, node):
        """
        先左旋转 然后右旋转调整节点node
        :param node: 待调整节点
        :return: None
        """
        self.left_rotate(node.left)
        self.right_rotate(node)

    def right_left_rotate(self, node):
        """
        先右旋转 然后左旋转调整节点node
        :param node: 待调整节点
        :return: node
        """
        self.right_rotate(node.right)
        self.left_rotate(node)


def test_avl_insert():
    value_list = [50, 25, 10, 5, 7, 3, 30, 20, 8, 15]
    avl = AVLTree(value_list)
    node_text_map, edges = avl.get_show_info()
    GraphVisual.GraphVisualization.show(node_text_map, edges, view_graph=True)


def test_avl_remove():
    value_list = [50, 25, 10, 5, 7, 3, 30, 20, 8, 15]
    avl = AVLTree(value_list)
    avl.remove_by_recursion(30)
    avl.remove_by_recursion(3)
    avl.remove_by_recursion(5)
    avl.remove_by_recursion(8)
    node_text_map, edges = avl.get_show_info()
    GraphVisual.GraphVisualization.show(node_text_map, edges, view_graph=True)


def test_random_insert(case_count=100, each_case_length=1000):
    def visit_func(tree_node, param):
        if tree_node:
            param[0].append(tree_node.data)
            param[1].append(tree_node.bf)
    is_all_case_ok = True
    for i in range(1, case_count + 1):
        value_list = random.sample(xrange(1000000000), each_case_length)
        avl = AVLTree(value_list)
        node_val_list = []
        node_bf_list = []
        avl.in_order_traverse_by_morris(visit_func, (node_val_list, node_bf_list))
        expected_result = sorted(node_val_list)
        result_status = True
        if node_val_list != expected_result:
            result_status = False
            print('Test case', i, ' in order traverse result: ', node_val_list, ' expected: ', expected_result)
        else:
            for bf in node_bf_list:
                if bf not in [-1, 0, 1]:
                    print('Test case', i, ' balance factor error bf=', bf)
                    result_status = False
                    break
        if result_status:
            print('Test case ', i, 'OK')
        else:
            print('Test case ', i, 'Error found in algorithm.')
            is_all_case_ok = False
    print('is all case passed ?', is_all_case_ok)


def test_random_remove(case_count=100, each_case_length=1000):
    def visit_func(tree_node, param):
        if tree_node:
            param[0].append(tree_node.data)
            param[1].append(tree_node.bf)
    is_all_case_ok = True
    for i in range(1, case_count + 1):
        value_list = random.sample(xrange(1000000000), each_case_length)
        avl = AVLTree(value_list)
        random.shuffle(value_list)
        result_status = True
        for x in value_list:
            avl.remove_by_recursion(x)
            node_val_list = []
            node_bf_list = []
            avl.in_order_traverse_by_morris(visit_func, (node_val_list, node_bf_list))
            expected_result = sorted(node_val_list)
            if node_val_list != expected_result:
                result_status = False
                print('Test case', i, ' in order traverse result: ', node_val_list, ' expected: ', expected_result)
            else:
                for bf in node_bf_list:
                    if bf not in [-1, 0, 1]:
                        print('Test case', i, ' balance factor error bf=', bf)
                        result_status = False
                        break
            if not result_status:
                break
        if result_status:
            print('Test case ', i, 'OK')
        else:
            print('Test case ', i, 'Error found in algorithm.')
            is_all_case_ok = False

    print('is all case passed ?', is_all_case_ok)


if __name__ == "__main__":
    test_random_remove()