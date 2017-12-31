#!/usr/bin/python
# -*- coding: UTF-8 -*-
import GraphVisual


class TreeNode(object):
    """
    二叉树节点
    """
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left, self.right = left, right

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return self.__str__()


class BinaryTree(object):
    """
       二叉树
    """
    def __init__(self):
        self.root = None

    def __init__(self, data_array):
        if type(data_array) is not list:
            raise ValueError("init with data array only.")
        if not data_array:
            self.root = None
            return
        self.root = TreeNode(data_array.pop(0))
        node_queue = [self.root]
        node_count = 1
        while data_array:
            next_node_count = 0
            while node_count > 0:
                node = node_queue.pop(0)
                node_count -= 1
                if data_array:
                    left_child_val = data_array.pop(0)
                    if left_child_val:
                        node.left = TreeNode(left_child_val)
                        node_queue.append(node.left)
                        next_node_count += 1
                if data_array:
                    right_child_val = data_array.pop(0)
                    if right_child_val:
                        node.right = TreeNode(right_child_val)
                        node_queue.append(node.right)
                        next_node_count += 1
            node_count = next_node_count

    def pre_order_traverse_by_recursion(self, traverse_func, func_param=None):
        """
        先序遍历 root - leftChild - rightChild
        递归实现
        :param traverse_func: 遍历函数
        :param func_param : 遍历函数的额外参数
        :return: None
        """
        BinaryTree.__pre__order_traverse__(self.root, traverse_func, func_param)

    @staticmethod
    def __pre__order_traverse__(node, traverse_func, param):
        if not node:
            return
        traverse_func(node, param)
        if node.left:
            BinaryTree.__pre__order_traverse__(node.left, traverse_func, param)
        if node.right:
            BinaryTree.__pre__order_traverse__(node.right, traverse_func, param)

    def pre_order_traverse_by_stack(self, traverse_func, func_param=None):
        """
            先序遍历非递归实现 使用栈辅助实现
            算法思想：
            1) 根节点入栈
            2) 取栈顶元素并访问它,并持续访问它的左孩子节点，过程中如果有右孩子节点则入栈
            3) 当步骤2找不到左孩子时，栈空则结束;否则继续步骤2
            :param traverse_func: 遍历函数
            :param func_param: 遍历函数的参数
            :return: None
        """
        if not self.root:
            return
        stack = [self.root]
        while stack:
            node = stack.pop(-1)
            while node:
                traverse_func(node, func_param)
                if node.right:
                    stack.append(node.right)
                node = node.left

    def in_order_traverse_by_recursion(self, traverse_func, func_param=None):
        """
        中序遍历 leftChild - root - rightChild
        :param traverse_func: 遍历函数
        :param func_param: 遍历函数的参数
        :return: None
        """
        BinaryTree.__in__order_traverse(self.root, traverse_func, func_param)

    @staticmethod
    def __in__order_traverse(node, traverse_func, func_param):
        if not node:
            return
        if node.left:
            BinaryTree.__in__order_traverse(node.left, traverse_func, func_param)
        traverse_func(node, func_param)
        if node.right:
            BinaryTree.__in__order_traverse(node.right, traverse_func, func_param)

    def in_order_traverse_by_stack(self, traverse_func, func_param=None):
        """
        中序遍历非递归实现 使用栈辅助实现
        算法思想：
        1) 将根节点设为当前待“归左”的节点
        2) 对待归左节点持续将左孩子节点入栈，直至左孩子为空，转步骤3
        3) 持续出栈，访问栈顶元素，直至当栈顶元素有右孩子时，将右孩子设为待“归左”节点，转步骤2;出栈过程中栈为空，则结束
        :param traverse_func: 遍历函数
        :param func_param: 遍历函数的参数
        :return: None
        """
        if not self.root:
            return
        stack = []
        node = self.root
        while node:
            while node:
                stack.append(node)
                node = node.left
            next_process_node = None
            while stack and not next_process_node:
                node = stack.pop(-1)
                traverse_func(node, func_param)
                next_process_node = node.right
            node = next_process_node

    def post_order_traverse_by_recursion(self, traverse_func, func_param=None):
        """
        后序遍历 leftChild - rightChild - root
        :param traverse_func: 遍历函数
        :param func_param: 遍历函数参数
        :return: None
        """
        BinaryTree.__post_order_traverse__(self.root, traverse_func, func_param)

    @staticmethod
    def __post_order_traverse__(node, traverse_func, func_param):
        if not node:
            return
        if node.left:
            BinaryTree.__post_order_traverse__(node.left, traverse_func, func_param)
        if node.right:
            BinaryTree.__post_order_traverse__(node.right, traverse_func, func_param)
        traverse_func(node, func_param)

    def post_order_traverse_by_stack(self, traverse_func, func_param=None):
        """
        后序遍历非递归实现  使用栈辅助实现
        算法思想：
        1) 将根节点设为当前待“归左”的节点
        2) 对待归左节点持续将左孩子节点入栈，直至左孩子为空，转步骤3
        3) 当栈不空时，若栈顶没有右孩子或者有右孩子但刚刚访问过则持续出栈；
           否则将栈顶右孩子设为待“归左”节点，转步骤2;出栈过程中栈为空，则结束
        :param traverse_func: 遍历函数
        :param func_param: 遍历函数的参数
        :return: None
        """
        if not self.root:
            return
        stack = []
        node = self.root
        while node:
            while node:
                stack.append(node)
                node = node.left
            next_process_node, prev_visit_node = None, None
            while stack and not next_process_node:
                top_node = stack[-1]
                if not top_node.right or prev_visit_node == top_node.right:
                    top_node = stack.pop(-1)
                    traverse_func(top_node, func_param)
                    prev_visit_node = top_node
                else:
                    next_process_node = top_node.right
            node = next_process_node

    def breadth_first_traverse(self, traverse_func, func_param=None):
        """
        广度优先遍历  使用队列辅助实现
        :param traverse_func: 遍历函数
        :param func_param: 遍历函数的参数
        :return: None
        """
        if not self.root:
            return
        queue = [self.root]
        while queue:
            front_node = queue.pop(0)
            traverse_func(front_node, func_param)
            if front_node.left:
                queue.append(front_node.left)
            if front_node.right:
                queue.append(front_node.right)

    def __str__(self, order="PreOrder"):

        def visit_func(tree_node, node_val_list):
            if tree_node:
                node_val_list.append(str(tree_node))
            else:
                node_val_list.append('NULL')

        tree_node_values = []
        if order == "PreOrder":
            self.pre_order_traverse_by_stack(visit_func, tree_node_values)
        elif order == "InOrder":
            self.in_order_traverse_by_stack(visit_func, tree_node_values)
        elif order == "PostOrder":
            self.post_order_traverse_by_stack(visit_func, tree_node_values)
        elif order == "BreadthFirst":
            self.breadth_first_traverse(visit_func, tree_node_values)
        ret_str = "BinaryTree " + order + " ["
        ret_str += ",".join(tree_node_values)
        ret_str += "]"
        return ret_str

    def __repr__(self):
        return self.__str__()

    def to_string(self, order="PreOrder"):
        return self.__str__(order)

    def get_node_edges(self):

        def visit_func(tree_node, param):
            if tree_node:
                param[0][str(id(tree_node))] = str(tree_node)
                if not tree_node.left and not tree_node.right:
                    return
                elif tree_node.left and tree_node.right:
                    param[1].append((str(id(tree_node)), str(id(tree_node.left)), True))
                    param[1].append((str(id(tree_node)), str(id(tree_node.right)), True))
                elif tree_node.left:
                    param[1].append((str(id(tree_node)), str(id(tree_node.left)), True))
                    # add a invisible dummy right node
                    dummy_node = TreeNode('NULL')
                    param[0][str(id(dummy_node))] = str(dummy_node)
                    param[1].append((str(id(tree_node)), str(id(dummy_node)), False))
                elif tree_node.right:
                    # add a invisible dummy left node
                    dummy_node = TreeNode('NULL')
                    param[0][str(id(dummy_node))] = str(dummy_node)
                    param[1].append((str(id(tree_node)), str(id(dummy_node)), False))
                    # add right node
                    param[1].append((str(id(tree_node)), str(id(tree_node.right)), True))

        node_2_text, edges_list = {}, []
        self.pre_order_traverse_by_recursion(visit_func, (node_2_text, edges_list))
        return node_2_text, edges_list


if __name__ == "__main__":
    data_val_list = ['A', 'B', 'C', 'D', 'F', 'G', 'H', 'I', 'J', None, None, None, 'K']
    # data_val_list = ['-', '+', '/', 'a', '*', 'e', 'f', None, None, 'b', '-', None, None, None, None, None, None, 'c', 'd']
    binary_tree = BinaryTree(data_val_list)
    print(binary_tree.to_string("PreOrder"))
    print(binary_tree.to_string("InOrder"))
    print(binary_tree.to_string("PostOrder"))
    print(binary_tree.to_string("BreadthFirst"))
    node_text_map, edges = binary_tree.get_node_edges()
    GraphVisual.TreeVisualization.show_tree(node_text_map, edges, view=True)

