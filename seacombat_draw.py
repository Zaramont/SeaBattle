import tkinter

# глобальные переменные - виджеты
root = None
canvas = None
# другие глобальные переменные
cell_side = 25
background_color = '#f7f2ff'
lines_color = '#c4bfcc'
draw_color = '#6521d1'
field1_left_x = field1_left_y = 50
field2_left_x = 14 * 25
field2_left_y = 50
white_rectangle = "#FFFFFF"
black_rectangle = '#000000'
field = None
field2 = None


def create_grid(w, h):
    for i in range(0, w, cell_side):
        canvas.create_line(i, 0, i, h, fill=lines_color)

    for i in range(0, h, cell_side):
        canvas.create_line(0, i, w, i, fill=lines_color)
    canvas.pack(fill=tkinter.BOTH, expand=True)


def init_gui():
    global root, canvas, w, h
    root = tkinter.Tk()
    root.title("SeaCombat")

    w = 26 * cell_side
    h = 14 * cell_side
    mw = root.winfo_screenwidth()
    mh = root.winfo_screenheight()
    root.geometry(
        "{}x{}+{}+{}".format(w, h, (mw - w) // 2, (mh - h) // 2))
    root.resizable(0, 0)

    canvas = tkinter.Canvas(master=root, background=background_color)
    canvas.pack(fill=tkinter.BOTH, expand=True)

    create_grid(w, h)
    draw_field(field1_left_x, field1_left_y, field)
    draw_field(field2_left_x, field2_left_y, field2)


def draw_field(coord_x, coord_y, field):
    canvas.create_rectangle(coord_x, coord_y, coord_x + cell_side * 10,
                            coord_y + cell_side * 10, width=3, outline=draw_color)
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K']

    for ix in range(10):
        canvas.create_text(coord_x + cell_side * ix + cell_side / 2, coord_y - cell_side / 2, text=letters[ix],
                           fill=draw_color)
        canvas.create_text(coord_x - cell_side / 2, coord_y + cell_side * ix + cell_side / 2, text=ix + 1,
                           fill=draw_color)
    for r in range(1, 11):
        for c in range(1, 11):
            if field[r][c] in [1, 2, 3, 4]:
                canvas.create_rectangle(coord_x + cell_side * (r - 1), coord_y + cell_side * (c - 1),
                                        coord_x + cell_side * r, coord_y + cell_side * c,
                                        width=3, outline=draw_color)

def start(f1, f2):
    global field,field2
    field = f1
    field2 = f2
    init_gui()
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
