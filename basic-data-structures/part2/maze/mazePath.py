#!/usr/bin/python
# -*- coding: UTF-8 -*-

import turtle
import sys

"""
迷宫路径问题
Author: wangdingqiao    http://blog.csdn.net/wangdingqiaoit
Date:2017-12-10
"""


class MazeCellNode(object):

    def __init__(self, pos_tuple):
        self.row = pos_tuple[0]
        self.col = pos_tuple[1]
        self.try_dir = 3

    def __str__(self):
        return "(" + str(self.row) + ","+str(self.col) + ")"

    def __repr__(self):
        return self.__str__()


class MazeGraphics(object):
    CELL_WIDTH = 50
    CELL_HEIGHT = 50
    MAX_ROW = 12
    MAX_COLUMN = 12

    def __init__(self):
        """Turtle Constructor"""
        self.mazeData = []
        self.path = []
        self.enter_pos = None
        self.dimension = None
        self.visited_map = {}

        self.screen = turtle.Screen()
        self.screen.title("Maze Program")
        self.screen.screensize(MazeGraphics.MAX_COLUMN * MazeGraphics.CELL_WIDTH,
                               MazeGraphics.MAX_ROW * MazeGraphics.CELL_HEIGHT)
        self.screen.setup(1000, 700, startx=0, starty=0)
        self.draw_start_pos = (0, 0)
        self.screen.bgcolor("orange")
        self.turtle = turtle.Turtle(shape="turtle")
        self.turtle.pensize(3)
        self.turtle.shapesize(2, 2)

    def read_from_file(self, file_name):
        with open(file_name, "r") as f:
            for i, line in enumerate(f.read().splitlines()):
                row = [x for x in line]
                self.mazeData.append(row)
                if 'I' in line:
                    self.enter_pos = (i, line.index('I'))
        if self.mazeData:
            self.dimension = (len(self.mazeData), len(self.mazeData[0]))
            self.draw_start_pos = (-self.dimension[1] / 2 * MazeGraphics.CELL_WIDTH,
                                   self.dimension[0] / 2 * MazeGraphics.CELL_HEIGHT)
            print('load maze file= ', file_name, " success dimension= ", self.dimension)

    def is_block_cell(self, x, y):
        return self.mazeData[x][y] == "1"

    def is_exit_cell(self, x, y):
        return self.mazeData[x][y] == "O"

    def is_enter_cell(self, x, y):
        return self.mazeData[x][y] == "I"

    def get_path(self):
        if not self.mazeData or not self.dimension:
            return
        self.path = []
        self.path.append(MazeCellNode(self.enter_pos))
        self.visited_map = {self.enter_pos: True}
        while self.path:
            cell_node = self.path[-1]
            if self.is_exit_cell(cell_node.row, cell_node.col):
                return self.path
            else:
                neighbor_pos = self.try_next_pos(cell_node)
                if not neighbor_pos:   # 相邻位置已经都尝试过了 则从路径中移除
                    self.path.pop()
                    self.visited_map[(cell_node.row, cell_node.col)] = False
                else:
                    self.path.append(MazeCellNode(neighbor_pos))    # 未访问过且有效则加入路径
                    self.visited_map[neighbor_pos] = True
        return None

    def solve_maze(self):
        if not self.mazeData or not self.dimension:
            return
        self.draw_maze()
        self.draw_text(self.draw_start_pos[0], - self.draw_start_pos[1] - 60, "Searching solution ...")
        self.path = []
        self.path.append(MazeCellNode(self.enter_pos))
        self.visited_map = {self.enter_pos: True}
        while self.path:
            cell_node = self.path[-1]
            if self.is_exit_cell(cell_node.row, cell_node.col):
                self.turtle.hideturtle()
                self.draw_text(self.draw_start_pos[0], - self.draw_start_pos[1] - 80,
                               "Path has Found!")
                self.turtle.penup()
                x, y = self.get_cell_pos(cell_node.row, cell_node.col)
                self.turtle.setpos(x + MazeGraphics.CELL_WIDTH / 2, y - MazeGraphics.CELL_HEIGHT / 2)
                self.turtle.showturtle()
                return self.path
            else:
                neighbor_pos = self.try_next_pos(cell_node)
                if not neighbor_pos:   # 相邻位置已经都尝试过了 则从路径中移除
                    self.path.pop()
                    self.visited_map[(cell_node.row, cell_node.col)] = False
                    from_pos = (cell_node.row, cell_node.col)
                    to_pos = None
                    if self.path:
                        to_pos = (self.path[-1].row, self.path[-1].col)
                else:
                    self.path.append(MazeCellNode(neighbor_pos))    # 未访问过且有效则加入路径
                    self.visited_map[neighbor_pos] = True
                    from_pos = (cell_node.row, cell_node.col)
                    to_pos = neighbor_pos
                self.fill_cell(from_pos, to_pos)
        self.draw_text(self.draw_start_pos[0], - self.draw_start_pos[1] - 80, "No Available Path!")
        return None

    def try_next_pos(self, maze_node):
        the_neighbor_pos, the_neighbor_dir = None, None
        offsets = [(-1, 0), (0, -1), (1, 0), (0, 1)]  # offset of one step toward [north, west, south, east]
        while not the_neighbor_pos and maze_node.try_dir >= 0:
            offset_row, offset_col = offsets[maze_node.try_dir][0], offsets[maze_node.try_dir][1]
            row, col = (maze_node.row + offset_row, maze_node.col + offset_col)
            maze_node.try_dir -= 1
            # print('try next pos of node', maze_node, "get pos", neighbor_pos)
            if row < 0 or col < 0 or row > self.dimension[0] or col > self.dimension[1]:
                continue
            if (row, col) in self.visited_map:
                continue
            if self.is_block_cell(row, col):
                continue
            the_neighbor_pos = (row, col)
            break
        # print('try next pos of node', maze_node, "final get pos", the_neighbor_pos)
        return the_neighbor_pos

    def draw_maze(self):
        if not self.dimension:
            return
        self.turtle.hideturtle()
        self.draw_text(self.draw_start_pos[0], - self.draw_start_pos[1] - 20, "Maze Path Program (By Wangdingqiao 2017)")
        self.draw_text(self.draw_start_pos[0], - self.draw_start_pos[1] - 40, "Initializing Maze ...")
        row, col = self.dimension[0], self.dimension[1]
        start_x, start_y = self.draw_start_pos[0], self.draw_start_pos[1]
        self.turtle.speed(0)
        self.turtle.begin_fill()
        self.draw_square(start_x, start_y,
                         col * MazeGraphics.CELL_WIDTH,
                         row * MazeGraphics.CELL_HEIGHT, "pink")
        self.turtle.end_fill()
        for i in range(row):
            self.turtle.penup()
            self.turtle.setpos(start_x, start_y - i * MazeGraphics.CELL_HEIGHT)
            self.turtle.pendown()
            for j in range(col):
                x, y = start_x + j * MazeGraphics.CELL_WIDTH, start_y - i * MazeGraphics.CELL_HEIGHT
                cell_color = self.get_cell_color(i, j)
                self.draw_square(x, y, MazeGraphics.CELL_WIDTH, MazeGraphics.CELL_HEIGHT, cell_color)
        self.turtle.showturtle()

    def get_cell_pos(self, row, col):
        start_x, start_y = self.draw_start_pos[0], self.draw_start_pos[1]
        x, y = start_x + col * MazeGraphics.CELL_WIDTH, start_y - row * MazeGraphics.CELL_HEIGHT
        return x, y

    def fill_cell(self, from_pos, to_pos):
        x, y = self.get_cell_pos(from_pos[0], from_pos[1])
        heading_dir = [90, 180, 270, 0]
        self.turtle.hideturtle()
        self.turtle.penup()
        self.turtle.setpos(x, y)
        self.turtle.pendown()
        self.turtle.speed(10)
        self.draw_square(x, y,
                         MazeGraphics.CELL_WIDTH,
                         MazeGraphics.CELL_HEIGHT,
                         self.get_cell_color(from_pos[0], from_pos[1]))
        self.turtle.penup()
        self.turtle.showturtle()
        self.turtle.color("black")
        self.turtle.setpos(x + MazeGraphics.CELL_WIDTH / 2, y - MazeGraphics.CELL_HEIGHT / 2)

        move_dir = self.get_move_dir(from_pos, to_pos)
        self.turtle.setheading(heading_dir[move_dir])
        self.screen.delay(40)
        self.turtle.speed(3)
        if move_dir == 0 or move_dir == 2:
            self.turtle.forward(MazeGraphics.CELL_HEIGHT)
        else:
            self.turtle.forward(MazeGraphics.CELL_WIDTH)
        self.turtle.pendown()

    def get_move_dir(self, from_pos, to_pos):
        offsets = [(-1, 0), (0, -1), (1, 0), (0, 1)]  # offset of one step toward [north, west, south, east]
        offset = (to_pos[0] - from_pos[0], to_pos[1] - from_pos[1])
        return offsets.index(offset)

    def draw_text(self, x, y, text_content):
        self.turtle.penup()
        self.turtle.setpos(x, y)
        self.turtle.color("black")
        self.turtle.write(text_content, font=("Arial", 13, "bold"))
        self.turtle.pendown()

    def get_cell_color(self, x, y):
        if self.is_block_cell(x, y):
            return "black"
        elif self.is_enter_cell(x, y):
            return "blue"
        elif self.is_exit_cell(x, y):
            return "red"
        elif (x, y) in self.visited_map and self.visited_map[(x, y)]:
            return "green"
        else:
            return "white"

    def draw_square(self, x, y, width, height, cell_color="red"):
        self.turtle.penup()
        self.turtle.setpos(x, y)
        self.turtle.setheading(0)
        self.turtle.pencolor("pink")
        self.turtle.pendown()
        # draw border
        for i in range(4):
            if i % 2 == 0:
                self.turtle.forward(width)
            else:
                self.turtle.forward(height)
            self.turtle.right(90)
        # fill inner area
        self.turtle.setpos(x+1, y+1)
        self.turtle.fillcolor(cell_color)
        self.turtle.begin_fill()
        for i in range(4):
            if i % 2 == 0:
                self.turtle.forward(width-1)
            else:
                self.turtle.forward(height-1)
            self.turtle.right(90)
        self.turtle.end_fill()

    def run_main_loop(self):
        turtle.mainloop()


if __name__ == "__main__":
    maze = MazeGraphics()
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        file_name = raw_input("input the path of the maze file to read:")
    maze.read_from_file(file_name)
    path = maze.solve_maze()
    print('found path?', str(path))
    maze.run_main_loop()
