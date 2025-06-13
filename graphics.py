from tkinter import Tk, BOTH, Canvas

class Cell():
    def __init__(self, win):
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
        point_top_left = Point(self.__x1, self.__y1)
        point_bottom_left = Point(self.__x1, self.__y2)
        point_top_right = Point(self.__x2, self.__y1)
        point_bottom_right = Point(self.__x2, self.__y2)
        if self.has_left_wall:
            self.__win.draw_line(Line(point_top_left, point_bottom_left))
        if self.has_right_wall:
            self.__win.draw_line(Line(point_top_right, point_bottom_right))
        if self.has_top_wall:
            self.__win.draw_line(Line(point_top_left, point_top_right))
        if self.has_bottom_wall:
            self.__win.draw_line(Line(point_bottom_left, point_bottom_right))

    def draw_move(self, to_cell, undo=False):
        temp_self = Line(self.__p1, self.__p2)
        temp_other = Line(to_cell.__p1, to_cell.__p2)
        connect_line = Line(temp_self.middle(), temp_other.middle())
        if undo:
            self.__win.draw_line(connect_line, "grey")
        else:
            self.__win.draw_line(connect_line, "red")

    def __repr__(self):
        string = f"<Cell object> A=({self.__x1}, {self.__y1}) B=({self.__x2}, {self.__y2}) "
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
