from graphics import Window, Cell

def main():
    win = Window(1200, 600)
    
    generate = [
        [80, 10, 10, 0b0111],
        [80, 100, 10, 0b1011],
        [80, 200, 10, 0b1101],
        [80, 300, 10, 0b1110],
        [80, 400, 10, 0b1111],
        [160, 10, 200, 0b0011],
        [160, 200, 200, 0b0101],
        [160, 400, 200, 0b0110],
        [160, 600, 200, 0b1001],
        [160, 800, 200, 0b1010],
        [160, 1000, 200, 0b1100],

    ]

    for input in generate:
        cell = Cell(win)
        cell.change_coordinates(input[0], height=input[0] * 2, anchor_x=input[1], anchor_y=input[2])
        if not input[3] & 0b1000:
            cell.has_left_wall = False
        if not input[3] & 0b0100:
            cell.has_bottom_wall = False
        if not input[3] & 0b0010:
            cell.has_right_wall = False
        if not input[3] & 0b0001:
            cell.has_top_wall = False
        cell.draw()
    

    win.wait_for_close()



if __name__ == "__main__":
    main()