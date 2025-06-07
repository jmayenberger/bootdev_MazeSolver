from graphics import Window, Point, Line

def main():
    win = Window(800, 600)
    
    
    a, b, c, d = Point(0,0), Point(800, 600), Point(50, 100), Point(500, 300)
    l1, l2, l3, l4, l5, l6 = Line(a, b), Line(a, c), Line(a, d), Line(b, c), Line(b, d), Line(c, d)
    win.draw_line(l1, "black")
    win.draw_line(l2, "red")
    win.draw_line(l3, "green")
    win.draw_line(l4, "blue")
    win.draw_line(l5, "grey")
    win.draw_line(l6, "yellow")

    win.wait_for_close()



if __name__ == "__main__":
    main()