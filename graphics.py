import time
from tkinter import Tk, BOTH, Canvas
from const import SLEEP_TIME, DRAW_COLOR, UNDO_COLOR


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
    ):
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self.__cells = []
        self.__create_cells()
    
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
                self.__animate()
                column.append(newCell)
            self.__cells.append(column)

    def __animate(self):
        if self.__win is None:
            return
        self.__win.redraw()
        time.sleep(SLEEP_TIME)

class Cell():
    def __init__(self, win=None):
        self.__win = win
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
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
        if self.has_left_wall:
            line = Line(point_top_left, point_bottom_left)
            if self.__win is None:
                lines.append(line)
            else:
                self.__win.draw_line(line)
        if self.has_bottom_wall:
            line = Line(point_bottom_left, point_bottom_right)
            if self.__win is None:
                lines.append(line)
            else:
                self.__win.draw_line(line)
        if self.has_right_wall:
            line = Line(point_top_right, point_bottom_right)
            if self.__win is None:
                lines.append(line)
            else:
                self.__win.draw_line(line)
        if self.has_top_wall:
            line = Line(point_top_left, point_top_right)
            if self.__win is None:
                lines.append(line)
            else:
                self.__win.draw_line(line)
        
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
                return (connect_line, UNDO_COLOR)
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

    def draw_line(self, line, fill_color="black"):
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
    
    def draw(self, canvas, fill_color="black"):
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