import time
import random
from tkinter import Tk, BOTH, Canvas
from const import SLEEP_TIME, DRAW_COLOR, UNDO_COLOR, WALL_COLOR, BG_COLOR


class Maze():
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None,
    ):
        random.seed(seed)
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self.__cells = []
        self.__create_cells()
        self.__break_entrance_and_exit()
        self.__break_walls_r(0, 0)
        self.__reset_cells_visited()
    
    def __create_cells(self):
        for i in range(self.__num_cols):
            column = []
            for j in range(self.__num_rows):
                newCell = Cell(self.__win)
                newCell.change_coordinates(
                    length=self.__cell_size_x,
                    height= self.__cell_size_y,
                    anchor_x=self.__x1 + i * self.__cell_size_x,
                    anchor_y=self.__y1 + j * self.__cell_size_y)
                newCell.draw()
                self.__animate(SLEEP_TIME / 10)
                column.append(newCell)
            self.__cells.append(column)

    def __break_entrance_and_exit(self):
        self.__cells[0][0].has_left_wall = False
        self.__cells[0][0].draw()
        self.__cells[-1][-1].has_right_wall = False
        self.__cells[-1][-1].draw()

    def __break_walls_r(self, i, j):
        self.__cells[i][j].visited = True
        while True:
            possible_directions = []
            if i < self.__num_cols - 1 and not self.__cells[i + 1][j].visited:
                possible_directions.append("right")
            if i > 0 and not self.__cells[i - 1][j].visited:
                possible_directions.append("left")
            if j < self.__num_rows - 1 and not self.__cells[i][j + 1].visited:
                possible_directions.append("bottom")
            if j > 0 and not self.__cells[i][j - 1].visited:
                possible_directions.append("top")
            
            if len(possible_directions) == 0:
                self.__cells[i][j].draw()
                return

            direction = possible_directions[random.randrange(len(possible_directions))]
            match direction:
                case "left":
                    self.__cells[i][j].has_left_wall = False
                    self.__cells[i - 1][j].has_right_wall = False
                    self.__break_walls_r(i - 1, j)
                case "right":
                    self.__cells[i][j].has_right_wall = False
                    self.__cells[i + 1][j].has_left_wall = False
                    self.__break_walls_r(i + 1, j)
                case "top":
                    self.__cells[i][j].has_top_wall = False
                    self.__cells[i][j - 1].has_bottom_wall = False
                    self.__break_walls_r(i, j - 1)
                case "bottom":
                    self.__cells[i][j].has_bottom_wall = False
                    self.__cells[i][j + 1].has_top_wall = False
                    self.__break_walls_r(i, j + 1)

    def __reset_cells_visited(self):
        for col in self.__cells:
            for cell in col:
                cell.visited = False

    def solve(self):
        return self.__solve_r(0, 0)
    
    def __solve_r(self, i, j):
        self.__animate()
        current_cell = self.__cells[i][j]
        current_cell.visited = True

        if i == self.__num_cols - 1 and j == self.__num_rows - 1:
            return True
        
        possible_directions = []
        if i < self.__num_cols - 1 and not self.__cells[i + 1][j].visited and not current_cell.has_right_wall:
            possible_directions.append("right")
        if j > 0 and not self.__cells[i][j - 1].visited and not current_cell.has_top_wall:
            possible_directions.append("top")
        if i > 0 and not self.__cells[i - 1][j].visited and not current_cell.has_left_wall:
            possible_directions.append("left")
        if j < self.__num_rows - 1 and not self.__cells[i][j + 1].visited and not current_cell.has_bottom_wall:
            possible_directions.append("bottom")

        for direction in possible_directions:
            match direction:
                case "left":
                    next_index = (i - 1, j)
                case "top":
                    next_index = (i, j - 1)
                case "right":
                    next_index = (i + 1, j)
                case "bottom":
                    next_index = (i, j + 1)
            next_cell = self.__cells[next_index[0]][next_index[1]]
            current_cell.draw_move(next_cell)
            if self.__solve_r(*next_index):
                return True
            else:
                current_cell.draw_move(next_cell, undo=True)
        
        return False

    def __animate(self, sleep=SLEEP_TIME):
        if self.__win is None:
            return
        self.__win.redraw()
        time.sleep(sleep)

class Cell():
    def __init__(self, win=None):
        self.__win = win
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
        self.__x1 = -1
        self.__x2 = -1
        self.__y1 = -1
        self.__y2 = -1
        self.__p1 = Point(self.__x1, self.__y1)
        self.__p2 = Point(self.__x2, self.__y2)

    def change_coordinates(self, length, anchor_point=None, height=None, anchor_x=0, anchor_y=0):
        if height is None:
            height = length
        if anchor_point is None:
            anchor_point = Point(anchor_x, anchor_y)
        self.__x1 = anchor_point.x
        self.__y1 = anchor_point.y
        self.__x2 = anchor_point.x + length
        self.__y2 = anchor_point.y + height
        self.__p1 = anchor_point
        self.__p2 = Point(self.__x2, self.__y2)

    def draw(self):
        point_top_left = self.__p1
        point_bottom_left = Point(self.__x1, self.__y2)
        point_top_right = Point(self.__x2, self.__y1)
        point_bottom_right = self.__p2
        lines = []

        line = Line(point_top_left, point_bottom_left)
        color = BG_COLOR
        if self.has_left_wall:
            color = WALL_COLOR
            lines.append(line)
        if self.__win is not None:
            self.__win.draw_line(line, color)

        line = Line(point_bottom_left, point_bottom_right)
        color = BG_COLOR
        if self.has_bottom_wall:
            color = WALL_COLOR
            lines.append(line)
        if self.__win is not None:
            self.__win.draw_line(line, color)
    
        line = Line(point_bottom_right, point_top_right)
        color = BG_COLOR
        if self.has_right_wall:
            color = WALL_COLOR
            lines.append(line)
        if self.__win is not None:
            self.__win.draw_line(line, color)

        line = Line(point_top_right, point_top_left)
        color = BG_COLOR
        if self.has_top_wall:
            color = WALL_COLOR
            lines.append(line)
        if self.__win is not None:
            self.__win.draw_line(line, color)
        
        return lines

    def draw_move(self, to_cell, undo=False):
        temp_self = Line(self.__p1, self.__p2)
        temp_other = Line(to_cell.__p1, to_cell.__p2)
        connect_line = Line(temp_self.middle(), temp_other.middle())
        if undo:
            if self.__win is None:
                return (connect_line, UNDO_COLOR)
            else:
                self.__win.draw_line(connect_line, UNDO_COLOR)
        else:
            if self.__win is None:
                return (connect_line, DRAW_COLOR)
            else:
                self.__win.draw_line(connect_line, DRAW_COLOR)

    def get_points(self):
        return (self.__p1, self.__p2)

    def __repr__(self):
        string = f"<Cell object> A={({self.__x1}, {self.__y1})} B=({self.__x2}, {self.__y2}) "
        if self.has_left_wall:
            string += "has_left_wall "
        if self.has_bottom_wall:
            string += "has_bottom_wall "
        if self.has_right_wall:
            string += "has_right_wall "
        if self.has_top_wall:
            string += "has_top_wall "
        return string

class Window():
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update()
        self.__root.update_idletasks()
    
    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("window closed...")

    def close(self):
        self.__running = False

    def draw_line(self, line, fill_color=WALL_COLOR):
        line.draw(self.__canvas, fill_color)

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        if isinstance(other, Point):
            return ((self.x == other.x and self.y == other.y)
                or (self.x == other.y and self.y == other.x))
        if isinstance(other, Line):
            return other == self
        return False

    def __sub__(self, other):
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y)
        return NotImplemented
    
    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        return NotImplemented 

    def __repr__(self):
        return f"<Point object> ({self.x}, {self.y})"

class Line():
    def __init__(self, p1, p2):
        self.__p1 = p1
        self.__p2 = p2
    
    def draw(self, canvas, fill_color=WALL_COLOR):
        canvas.create_line(self.__p1.x, self.__p1.y, self.__p2.x, self.__p2.y, fill=fill_color, width=2)

    def middle(self):
        x = abs(self.__p1.x + self.__p2.x) / 2
        y = abs(self.__p1.y + self.__p2.y) / 2
        return Point(x, y)
    
    def get_points(self):
        return (self.__p1, self.__p2)

    def __eq__(self, other):
        if isinstance(other, Line):
            (op1, op2) = other.get_points()
        elif isinstance(other, Point):
            op1 = other
            op2 = other
        else:
            return False
        return ((self.__p1 == op1 and self.__p2 == op2)
                or (self.__p1 == op2 and self.__p2 == op1))

    def __sub__(self, other):
        if isinstance(other, Point):
            return Line(self.__p1 - other, self.__p2 - other)
        if isinstance(other, Line):
            (op1, op2) = other.get_points()
            return Line(self.__p1 - op1, self.__p2 - op2)
        return NotImplemented
    
    def __add__(self, other):
        if isinstance(other, Point):
            return Line(self.__p1 + other, self.__p2 + other)
        if isinstance(other, Line):
            (op1, op2) = other.get_points()
            return Line(self.__p1 + op1, self.__p2 + op2)
        return NotImplemented

    def __repr__(self):
        return f"<Line object> from {repr(self.__p1)} to {repr(self.__p2)}"