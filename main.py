from graphics import Window, Maze

def main():
    win = Window(1200, 600)
    
    maze = Maze(
        x1=10,
        y1=10,
        num_rows=20,
        num_cols=30,
        cell_size_x=100,
        cell_size_y=50,
        win=win
    )

    win.wait_for_close()



if __name__ == "__main__":
    main()