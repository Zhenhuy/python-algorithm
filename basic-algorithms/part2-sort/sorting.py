#!/usr/env/python
# _*_ coding: utf-8 _*_

"""
排序算法
reference-link:
[1]-https://sites.fas.harvard.edu/~cscie119/lectures/sorting.pdf
[2]-https://en.wikipedia.org/wiki/Shellsort
[3]-https://en.wikipedia.org/wiki/Quicksort
[4]-https://www.geeksforgeeks.org/hoares-vs-lomuto-partition-scheme-quicksort/
"""


class Sort(object):

    @staticmethod
    def __index_of_selection__(input_array, start, end, descend_order=False):
        if not input_array:
            raise ValueError("input array is empty.")
        if start < 0 \
                or end < 0 \
                or start > end \
                or end >= len(input_array):
            raise AssertionError("invalid array index", start, end)
        select_index = start
        for i in range(start + 1, end + 1):
            if descend_order:           # 降序排列时选择次大元素
                if input_array[i] > input_array[select_index]:
                    select_index = i
            elif input_array[i] < input_array[select_index]:
                select_index = i
        return select_index

    @staticmethod
    def __swap_element__(input_array, index_left, index_right):
        if not input_array:
            raise ValueError("input array is empty.")
        if index_left < 0 \
                or index_right < 0 \
                or index_left >= len(input_array) \
                or index_right >= len(input_array):
            raise AssertionError("invalid array index", index_left, index_right)
        if index_left != index_right:
            input_array[index_left], input_array[index_right] = input_array[index_right], input_array[index_left]

    @staticmethod
    def selection_sort(input_array, descend_order=False):
        """
        选择排序
        依次从[0,len-1]位置选择应该放在这个位置上的那个最小或者最大元素
        :param input_array: 输入元素列表
        :param descend_order: 是否降序排列
        :return: None
        """
        for i in range(len(input_array)-1):
            select_index = Sort.__index_of_selection__(input_array, i, len(input_array) - 1, descend_order)
            if i != select_index:
                Sort.__swap_element__(input_array, i, select_index)
            print("after ", i+1, " select: ", input_array)

    @staticmethod
    def insertion_sort(input_array, descend_order=False):
        """
        插入排序
        依次将[1,len-1]位置元素插入在适当位置
        :param input_array: 输入元素列表
        :param descend_order: 是否降序排列
        :return: None
        """
        for i in range(1, len(input_array)):
            to_insert = input_array[i]
            j = i
            if descend_order:
                while j > 0 and input_array[j-1] < to_insert:  # 降序排列时小于插入元素的部分后移
                    input_array[j] = input_array[j-1]
                    j -= 1
            else:
                while j > 0 and input_array[j-1] > to_insert:  # 升序排列时大于插入元素的部分后移
                    input_array[j] = input_array[j-1]
                    j -= 1
            if j != i:
                input_array[j] = to_insert
            print("after ", i, " insert: ", input_array)

    @staticmethod
    def shell_sort(input_array, descend_order=False):
        """
        希尔排序
        对插入排序的改进
        根据间隔序列(gap sequence)对子数组进行插入排序 间隔序列对排序效率有影响
        :param input_array: 输入元素列表
        :param descend_order: 是否降序排列
        :return: None
        """
        gap_seq = [701, 301, 132, 57, 23, 10, 4, 1]  # Using Marcin Ciura's gap sequence
        # gap_seq = [5, 3, 1]
        for gap in gap_seq:
            for i in range(gap, len(input_array)):
                to_insert = input_array[i]
                j = i
                if descend_order:
                    while j >= gap and input_array[j-gap] < to_insert:  # 降序排列时小于插入元素的部分后移
                        input_array[j] = input_array[j-gap]
                        j -= gap
                else:
                    while j >= gap and input_array[j-gap] > to_insert:  # 升序排列时大于插入元素的部分后移
                        input_array[j] = input_array[j-gap]
                        j -= gap
                if j != i:
                    input_array[j] = to_insert
            print('after gap= ', gap, " array is: ", input_array)

    @staticmethod
    def bubble_sort(input_array, descend_order=False):
        """
        冒泡排序
        进行len-1趟冒泡过程，每次将最大(或者最小元素)交换到最终位置
        :param input_array: 输入元素列表
        :param descend_order: 是否降序排列
        :return: None
        """
        for j in range(len(input_array)-1, 0, -1):
            for i in range(j):
                if descend_order:  # 降序排列时 将最小元素交换到最终位置
                    if input_array[i] < input_array[i+1]:
                        Sort.__swap_element__(input_array, i, i + 1)
                else:             # 升序排列时 将最大元素交换到最终位置
                    if input_array[i] > input_array[i+1]:
                        Sort.__swap_element__(input_array, i, i + 1)

    @staticmethod
    def lomuto_partition(input_array, low, high, descend_order=False):
        """
        lomuto划分算法
        :param input_array: 输入数组
        :param low: 开始索引
        :param high: 停止索引
        :param descend_order: 是否降序排列
        :return: pivot所在索引pos 划分区间为[low, pos-1] [ pos+1, high]
        """
        if low < 0 \
                or high < 0 \
                or low >= len(input_array) \
                or high >= len(input_array):
            raise AssertionError("invalid array index", low, high)
        pivot = input_array[high]  # right most element as pivot
        print('lomuto partition choosing pivot= ', pivot)
        i = low - 1  # marker for element less than pivot
        for j in range(low, high):
            if descend_order:   # 降序排列 大的元素在左 小的元素在右
                if input_array[j] > pivot:
                    i += 1
                    Sort.__swap_element__(input_array, i, j)
            else:               # 升序排列 大的元素在右 小的元素在左
                if input_array[j] < pivot:
                    i += 1
                    Sort.__swap_element__(input_array, i, j)
        Sort.__swap_element__(input_array, i + 1, high)
        return i + 1

    @staticmethod
    def hoare_partition(input_array, low, high, descend_order=False):
        if low < 0 \
                or high < 0 \
                or low >= len(input_array) \
                or high >= len(input_array):
            raise AssertionError("invalid array index", low, high)
        pivot = input_array[(low + high) / 2]
        print('hoare partition choosing pivot= ', pivot)
        while True:
            if descend_order:   # 降序排列 大的元素在左 小的元素在右
                while low < high and input_array[low] > pivot:
                    low += 1
                while low < high and input_array[high] < pivot:
                    high -= 1
            else:               # 升序排列 大的元素在右 小的元素在左
                while low < high and input_array[low] < pivot:
                    low += 1
                while low < high and input_array[high] > pivot:
                    high -= 1
            if low < high:
                Sort.__swap_element__(input_array, low, high)
                low += 1
                high -= 1
            else:
                return high

    @staticmethod
    def quick_sort_lomuto(input_array, descend_order=False):
        """
        快速排序
        :param input_array: 输入元素列表
        :param descend_order: 是否降序排列
        :return: None
        """
        def quick_sort(in_array, low, high):
            pos = Sort.lomuto_partition(in_array, low, high, descend_order)
            if low < pos - 1:
                quick_sort(in_array, low, pos - 1)
            if pos + 1 < high:
                quick_sort(in_array, pos + 1, high)
        if input_array:
            quick_sort(input_array, 0, len(input_array)-1)

    @staticmethod
    def quick_sort_hoare(input_array, descend_order=False):
        """
        快速排序
        :param input_array: 输入元素列表
        :param descend_order: 是否降序排列
        :return: None
        """

        def quick_sort(in_array, low, high):
            pos = Sort.hoare_partition(in_array, low, high, descend_order)
            if low < pos:
                quick_sort(in_array, low, pos)
            if pos + 1 < high:
                quick_sort(in_array, pos + 1, high)

        if input_array:
            quick_sort(input_array, 0, len(input_array) - 1)


def test_case_1():
    input_array = [15, 6, 2, 12, 4]
    array_copy = [x for x in input_array]
    print("input array is: ", input_array)

    Sort.selection_sort(input_array)
    print(" selection sort by ascending order: ", input_array)
    Sort.selection_sort(array_copy, descend_order=True)
    print(" selection sort by descending order: ", array_copy)


def test_case_2():
    input_array = [12, 5, 2, 13, 18, 4]
    array_copy = [x for x in input_array]
    print("input array is: ", input_array)

    Sort.insertion_sort(input_array)
    print(" insertion sort by ascending order: ", input_array)
    Sort.insertion_sort(array_copy, descend_order=True)
    print(" insertion sort by descending order: ", array_copy)


def test_case_3():
    input_array = [62, 83, 18, 53, 07, 17, 95, 86, 47, 69, 25, 28]
    array_copy = [x for x in input_array]
    print("input array is: ", input_array)

    Sort.shell_sort(input_array)
    print(" shell sort by ascending order: ", input_array)
    Sort.shell_sort(array_copy, descend_order=True)
    print(" shell sort by descending order: ", array_copy)


def test_case_4():
    input_array = [28, 24, 27, 18]
    array_copy = [x for x in input_array]
    print("input array is: ", input_array)

    Sort.bubble_sort(input_array)
    print(" bubble sort by ascending order: ", input_array)
    Sort.bubble_sort(array_copy, descend_order=True)
    print(" bubble sort by descending order: ", array_copy)


def test_case_5():
    input_arrays = [[10, 80, 30, 90, 40, 50, 70], [7, 15, 4, 9, 6, 18, 9, 12]]
    for input_array in input_arrays:
        array_copy = [x for x in input_array]
        print("input array is: ", input_array)

        pos = Sort.lomuto_partition(input_array, 0, len(input_array)-1)
        print(" lomuto partition by ascending order: ", input_array, "split= ", pos)

        pos = Sort.lomuto_partition(array_copy, 0, len(array_copy) - 1, descend_order=True)
        print(" lomuto partition by descending order: ", array_copy, "split= ", pos)
        print("\n")


def test_case_6():
    input_arrays = [[10, 80, 30, 90, 40, 50, 70], [7, 15, 4, 9, 6, 18, 9, 12]]
    for input_array in input_arrays:
        array_copy = [x for x in input_array]
        print("input array is: ", input_array)

        pos = Sort.hoare_partition(input_array, 0, len(input_array)-1)
        print(" hoare partition by ascending order: ", input_array, "split= ", pos)

        pos = Sort.hoare_partition(array_copy, 0, len(array_copy) - 1, descend_order=True)
        print(" hoare partition by descending order: ", array_copy, "split= ", pos)
        print("\n")


def test_case_7():
    input_arrays = [[10, 80, 30, 90, 40, 50, 70], [7, 15, 4, 9, 6, 18, 9, 12]]
    for input_array in input_arrays:
        array_copy = [x for x in input_array]
        print("input array is: ", input_array)

        Sort.quick_sort_lomuto(input_array)
        print(" quick sort lomuto partition by ascending order: ", input_array)

        Sort.quick_sort_lomuto(array_copy, descend_order=True)
        print(" quick sort lomuto partition by descending order: ", array_copy)
        print("\n")


def test_case_8():
    input_arrays = [[10, 80, 30, 90, 40, 50, 70], [7, 15, 4, 9, 6, 18, 9, 12]]
    for input_array in input_arrays:
        # array_copy = [x for x in input_array]
        print("input array is: ", input_array)

        Sort.quick_sort_hoare(input_array)
        print(" quick sort hoare partition by ascending order: ", input_array)

        # Sort.quick_sort_hoare(array_copy, descend_order=True)
        # print(" quick sort hoare partition by descending order: ", array_copy)
        print("\n")


if __name__ == "__main__":
    test_case_8()