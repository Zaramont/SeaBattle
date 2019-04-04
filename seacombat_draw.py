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
    global root
    root = tkinter.Tk()
    root.title("SeaCombat")

    w = h = board_size
    mw = root.winfo_screenwidth()
    mh = root.winfo_screenheight()

    root.geometry("{}x{}+{}+{}".format(w + 220, h + 20, (mw - w) // 2, (mh - h) // 2))
    root.resizable(0, 0)

    container1 = tkinter.Frame(master=root)
    container1.place(x=0, y=0, width=w + 220, height=h + 20)

    canvas = tkinter.Canvas(master=container1, background=background_color)
    canvas.pack(fill=tkinter.BOTH, expand=True)


def draw_board():
    pass


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
