import tkinter

# глобальные переменные - виджеты
root = None
canvas = None
# другие глобальные переменные
board_size = 400
background_color = '#f8f4ff'

white_rectangle = "#FFFFFF"
black_rectangle = '#000000'


def init_gui():
    global root, container1, canvas, w, h
    root = tkinter.Tk()
    root.title("SeaCombat")

    w = h = board_size
    mw = root.winfo_screenwidth()
    mh = root.winfo_screenheight()

    root.geometry(
        "{}x{}+{}+{}".format(w + 220, h + 20, (mw - w) // 2, (mh - h) // 2))
    root.resizable(0, 0)

    container1 = tkinter.Frame(master=root)
    container1.place(x=0, y=0, width=w + 220, height=h + 20)

    canvas = tkinter.Canvas(master=container1, background=background_color)
    canvas.pack(fill=tkinter.BOTH, expand=True)


def draw_board(whitecolor=None, blackcolor=None):
    rect_side = 25
    coodr_x = coord_y = 50
    canvas.create_rectangle(coodr_x, coord_y, coodr_x + rect_side * 10,
                            coord_y + rect_side * 10)
    # canvas.create_rectangle(350,50,600,300)
    for r in range(1, 11):
        for c in range(1, 11):
            canvas.create_rectangle(coodr_x + (r - 1) * rect_side,
                                    coord_y + (c - 1) * rect_side,
                                    (coodr_x + (r - 1) * rect_side) + 25,
                                    (coord_y + (c - 1) * rect_side) + 25)

    canvas.create_rectangle(50, 50, 75, 75)


if __name__ == '__main__':
    init_gui()
    draw_board()

root.mainloop()


def show_battlefield(field):
    for r in range(len(field)):
        for c in range(len(field[r])):
            if field[r][c] == 9:
                field[r][c] = 'o'
            elif field[r][c] == 0:
                field[r][c] = "_"
            else:
                field[r][c] = "x"
    show_array(field)


def show_array(field):
    for r in field:
        print(r)
