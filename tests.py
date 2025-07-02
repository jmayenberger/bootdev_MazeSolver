import unittest
from graphics import Maze, Cell, Line, Point

class Tests(unittest.TestCase):
    def test_cell_change_coordinates(self):
        cell = Cell()
        length = []
        anchor_point = []
        height = []
        anchor_x = []
        anchor_y = []
        result = []

        length.append(5)
        anchor_point.append(None)
        height.append(None)
        anchor_x.append(0)
        anchor_y.append(0)
        result.append((Point(0,0), Point(5,5)))

        length.append(10)
        anchor_point.append(Point(2,3))
        height.append(3)
        anchor_x.append(7)
        anchor_y.append(8)
        result.append((Point(2,3), Point(12,6)))

        length.append(4)
        anchor_point.append(None)
        height.append(7)
        anchor_x.append(5)
        anchor_y.append(13)
        result.append((Point(5,13), Point(9,20)))

        for i in range(len(result)):
            cell.change_coordinates(length[i], anchor_point[i], height[i], anchor_x[i], anchor_y[i])
            self.assertEqual(
                cell.get_points(),
                result[i])
        print("Cell change_coordinates works as intended")

    def test_cell_draw(self):
        cell = Cell()
        length = 5
        height = 8
        anchor = Point(1,2)
        cell.change_coordinates(length, anchor, height)
        p1 = anchor
        p2 = Point(0, height) + anchor
        p3 = Point(length, height) + anchor
        p4 = Point(length, 0) + anchor
        lines = [Line(p1, p2), Line(p2, p3), Line(p3, p4), Line(p4, p1)]

        for i in range(0b1111 + 1):
            expect = []
            (cell.has_bottom_wall, cell.has_left_wall, cell.has_right_wall, cell.has_top_wall) = (False, False, False, False)
            if i & 0b0001:
                cell.has_left_wall = True
                expect.append(lines[0])
            if i & 0b0010:
                cell.has_bottom_wall = True
                expect.append(lines[1])
            if i & 0b0100:
                cell.has_right_wall = True
                expect.append(lines[2])
            if i & 0b1000:
                cell.has_top_wall = True
                expect.append(lines[3])
            drawn = cell.draw()
            for j in range(max(len(drawn), len(expect))):
                self.assertEqual(drawn[j], expect[j])
        print("Cell draw draws correct walls")

    def test_maze_create_cells(self):
        x1 = 0
        y1 = 0
        num_cols = 12
        num_rows = 10
        cell_size_x = 10
        cell_size_y = 11
        m1 = Maze(x1, y1, num_rows, num_cols, cell_size_x, cell_size_y)
        self.assertEqual(
            len(m1._Maze__cells), # type: ignore
            num_cols,
        )
        for i in range(num_cols):
            self.assertEqual(
                len(m1._Maze__cells[i]), # type: ignore
                num_rows,
            )
        print("Maze create_cells creates correct number of cells")

        testpoint = Point(x1 + cell_size_x, y1 + cell_size_y)
        for i in range(num_cols):
            for j in range(num_rows):
                cell = m1._Maze__cells[i][j] # type: ignore
                (p1, p2) = cell.get_points()
                self.assertEqual(
                    p2 - p1,
                    testpoint
                )
                self.assertEqual(
                    p1,
                    Point(x1 + i * cell_size_x, y1 + j * cell_size_y)
                )
        print("Maze create_cells creates correct cell coordinates")

    def test_maze_break_entrance_and_exit(self):
        x1 = 20
        y1 = 87
        num_cols = 8
        num_rows = 15
        cell_size_x = 7
        cell_size_y = 17
        m1 = Maze(x1, y1, num_rows, num_cols, cell_size_x, cell_size_y)
        self.assertEqual(m1._Maze__cells[0][0].has_left_wall, False) # type: ignore
        self.assertEqual(m1._Maze__cells[m1._Maze__num_cols - 1][m1._Maze__num_rows - 1].has_right_wall, False) # type: ignore
        print("Maze break_entrance_and_exit works as intended")

    def test_maze_reset_cells_visited(self):
        x1 = 5
        y1 = 100
        num_cols = 23
        num_rows = 6
        cell_size_x = 76
        cell_size_y = 64
        m1 = Maze(x1, y1, num_rows, num_cols, cell_size_x, cell_size_y)
        m1._Maze__cells[0][0].visited = True # type: ignore
        m1._Maze__cells[-1][-1].visited = True # type: ignore
        m1._Maze__reset_cells_visited() # type: ignore
        for i in range(num_cols):
            for j in range(num_rows):
                self.assertEqual(m1._Maze__cells[i][j].visited, False) # type: ignore
        print("Maze reset_cells_visited works as intended")


if __name__ == "__main__":
    unittest.main()