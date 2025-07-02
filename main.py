from graphics import Window, Maze

def main():
    width = 1200
    height = 600
    win = Window(width, height)
    
    x1 = 10
    y1 = 10
    num_rows = 20
    num_cols = 30
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

    win.wait_for_close()



if __name__ == "__main__":
    main()