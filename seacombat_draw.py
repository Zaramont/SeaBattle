import tkinter

root = None
canvas = None

cell_side = 25
background_color = '#f7f2ff'
lines_color = '#c4bfcc'
draw_color = '#3d0084'
field1_left_x = cell_side * 10
field2_left_x = 22 * cell_side
field1_left_y = field2_left_y = cell_side * 2

field = None
field2 = None


def create_grid(w, h):
    for i in range(0, w, cell_side):
        canvas.create_line(i, 0, i, h, fill=lines_color)

    for i in range(0, h, cell_side):
        canvas.create_line(0, i, w, i, fill=lines_color)
    canvas.pack(fill=tkinter.BOTH, expand=True)


def init_gui():
    global root, canvas
    root = tkinter.Tk()
    root.title("SeaCombat")

    w = 34 * cell_side
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


def draw_orange(event):
    r = 5
    canvas.create_oval(event.x - r, event.y - r,
                       event.x + r, event.y + r, fill='orange')


def create_ship(event):
    canvas.create_rectangle(event.x, event.y,
                            event.x + cell_side,
                            event.y + cell_side, width=3, outline=draw_color)  # .bind('Motion', lambda event2: canvas.move(event2.self, event2.x,event2.y))
    pass


def draw_list_of_ships():
    for ix in range(1, 5):
        canvas.create_text(cell_side * 2.5, cell_side * 0.5 + cell_side * ix * 2,
                           text=ix, fill=draw_color, width=3)
        canvas.create_text(cell_side * 3.5, cell_side * 0.5 + cell_side * ix * 2, text='x', fill=draw_color, width=3)
        # ship4 = tkinter.Canvas(root, bg=background_color)
        # ship4.place(x=cell_side * 4 + 2, y=cell_side * ix * 2 + 2, width=cell_side * (5 - ix) - 3, height=cell_side - 3)
        # ship4.bind('<Button-1>', create_ship)

        for q in range(5 - ix, 0, -1):
            left_x = q * cell_side + 3 * cell_side
            left_y = ix * 2 * cell_side
            canvas.create_rectangle(left_x, left_y,
                                    left_x + cell_side,
                                    left_y + cell_side,
                                    width=3, outline=draw_color, fill=background_color, tags='ship' + str(5 - ix))
            canvas.tag_bind('ship' + str(5 - ix), '<Button-1>', create_ship)
    pass


def draw_field(coord_x, coord_y, field):
    canvas.create_rectangle(coord_x - 1, coord_y - 1,
                            coord_x + 1 + cell_side * 10,
                            coord_y + 1 + cell_side * 10,
                            width=3, outline=draw_color)

    letters = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'К']
    for ix in range(10):
        canvas.create_text(coord_x + cell_side * ix + cell_side / 2,
                           coord_y - cell_side / 2, text=letters[ix],
                           fill=draw_color)
        canvas.create_text(coord_x - cell_side / 2,
                           coord_y + cell_side * ix + cell_side / 2,
                           text=ix + 1,
                           fill=draw_color)

    for r in range(1, 11):
        for c in range(1, 11):
            if field[r][c] in [1, 2, 3, 4]:  # remember this bug)
                # print("c= " + str(c) + " r= " + str(r))
                canvas.create_rectangle(coord_x + cell_side * (c - 1),
                                        coord_y + cell_side * (r - 1),
                                        coord_x + cell_side * c,
                                        coord_y + cell_side * r,
                                        width=3, outline=draw_color)


def start(f1, f2):
    try:
        global field, field2
        field = f1
        field2 = f2
        init_gui()
        draw_list_of_ships()
        root.mainloop()
    except Exception as e:
        print(e)


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
