from graphics import Window, Maze
from const import RECURSION_LIMIT, AWAIT
import sys
import time

def main():
    width = 1600
    height = 900
    win = Window(width, height)
    sys.setrecursionlimit(int(RECURSION_LIMIT))
    
    x1 = 10
    y1 = 10
    num_rows = 25
    num_cols = 17
    cell_size_x = (width - 2 * x1) / num_cols
    cell_size_y = (height - 2 * y1) / num_rows
    maze = Maze(
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win
    )

    time.sleep(AWAIT)

    if maze.solve():
        print("solved Maze succesfully")
    else:
        print("no solution found")

    win.wait_for_close()



if __name__ == "__main__":
    main()