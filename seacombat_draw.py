import math
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


def create_grid(w, h):
    for i in range(0, w, cell_side):
        canvas.create_line(i, 0, i, h, fill=lines_color)

    for i in range(0, h, cell_side):
        canvas.create_line(0, i, w, i, fill=lines_color)
    canvas.pack(fill=tkinter.BOTH, expand=True)


def draw_list_of_ships():
    size = 4
    ships = []
    while size > 0:

        canvas.create_text(cell_side * 2.5,
                           cell_side * 0.5 + cell_side * (5 - size) * 2,
                           text=5 - size, fill=draw_color, width=3)
        canvas.create_text(cell_side * 3.5,
                           cell_side * 0.5 + cell_side * (5 - size) * 2,
                           text='x',
                           fill=draw_color,
                           width=3)

        left_x = cell_side * 4
        left_y = 2 * cell_side * (5 - size)
        ships.append(canvas.create_rectangle(left_x, left_y, left_x + cell_side * size,
                                left_y + cell_side,
                                width=3, outline=draw_color,
                                fill=background_color,
                                tags='ship'))
        # lambda event: create_ship(event, size))
        # canvas.update()
        size -= 1
    return ships


def draw_field(coord_x, coord_y, field, tag):
    canvas.create_rectangle(coord_x - 1, coord_y - 1,
                            coord_x + 1 + cell_side * 10,
                            coord_y + 1 + cell_side * 10,
                            width=3, outline=draw_color, tags=tag)

    letters = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'К']
    for ix in range(10):
        canvas.create_text(coord_x + cell_side * ix + cell_side / 2,
                           coord_y - cell_side / 2, text=letters[ix],
                           fill=draw_color)
        canvas.create_text(coord_x - cell_side / 2,
                           coord_y + cell_side * ix + cell_side / 2,
                           text=ix + 1,
                           fill=draw_color)

    list_of_ships = []
    for size in field:
        list_of_ships.extend(field[size])
    for ship in list_of_ships:
        for deck in ship:
            c = deck[1]
            r = deck[0]
            canvas.create_rectangle(coord_x + cell_side * (c - 1),
                                    coord_y + cell_side * (r - 1),
                                    coord_x + cell_side * c,
                                    coord_y + cell_side * r,
                                    width=3, outline=draw_color)





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
    draw_field(field1_left_x, field1_left_y, field, 'player_field')
    draw_field(field2_left_x, field2_left_y, field2, 'ai_field')
    return canvas



def redraw_field(x, y, field3, tag):
    draw_field(x, y, field3, tag)


def start(f1, f2):
    try:
        global field, field2
        field = f1
        field2 = f2
        init_gui()
        draw_list_of_ships()
        # root.focus_set()
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
    print()
    for r in field:
        print(r)


def show_dict_field(field):
    field2 = [
        [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
        [9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9],
        [9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9],
        [9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9],
        [9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9],
        [9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9],
        [9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9],
        [9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9],
        [9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9],
        [9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9],
        [9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9],
        [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
    ]
    list_of_ships = []
    for i in field:
        list_of_ships.extend(field[i])
    for ship in list_of_ships:
        for deck in ship:
            field2[deck[0]][deck[1]] = len(ship)
    show_battlefield(field2)


def create_rectangle(event_x,event_y,tag):
    if canvas.coords('new_ship'):  # prevent creation of two new ships
        return

    ship = canvas.find_closest(event_x, event_y)
    ship_coords = canvas.coords(ship)
    ship_size = (ship_coords[2] - ship_coords[0]) / cell_side

    width = cell_side * ship_size
    x = event_x - width / 2
    y = event_y - cell_side / 2
    return canvas.create_rectangle(x, y,
                            x + cell_side * ship_size,
                            y + cell_side, width=3, outline=draw_color,
                            fill=background_color,
                            tags=tag)
