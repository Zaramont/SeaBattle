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


def change_rectangle_color(tag, color):
    elem = canvas.find_withtag(tag)[0]
    canvas.itemconfig(elem, outline=color)


def create_checkbox_for_enemy_field(x, y, command):
    global show_enemy_placement
    show_enemy_placement = tkinter.IntVar()
    C = tkinter.Checkbutton(root, text='Show enemy ships',
                            variable=show_enemy_placement, command=command)
    C.place(x=x, y=y)
    return C


def create_grid(x, y, w, h, color):
    for i in range(x + cell_side, w, cell_side):
        canvas.create_line(i, y, i, h, fill=color)

    for i in range(y+cell_side, h, cell_side):
        canvas.create_line(x, i, w, i, fill=color)
    # canvas.pack(fill=tkinter.BOTH, expand=True)


def create_menu(func, func2):
    menu = tkinter.Menu(root, relief=tkinter.RAISED)
    menu.add_command(label='New Game')
    menu.add_command(label='Save Game', command=func)
    menu.add_command(label='Load Game', command=func2)

    menu.add_command(label='Exit', command=root.quit)
    root.config(menu=menu)


def draw_borders(ship, coord_x, coord_y, tag):
    for deck in ship:
        r = deck[0]
        c = deck[1]
        canvas.create_rectangle(coord_x + cell_side * (c - 1),
                                coord_y + cell_side * (r - 1),
                                coord_x + cell_side * c,
                                coord_y + cell_side * r,
                                width=3, outline='red', tags='ship_' + tag)


def draw_button(x, y, height, width, text, command):
    B = tkinter.Button(root, text=text, command=command, bg=background_color)
    B.place(x=x, y=y, height=height, width=width)


def draw_cross(x, y, color, tag):
    canvas.create_line(x, y, x + cell_side, y + cell_side, fill=color, width=2)
    canvas.create_line(x + cell_side, y, x, y + cell_side, fill=color, width=2)


def draw_counter_of_ship(tag, size, quantity):
    if len(canvas.find_withtag(tag)) > 0:
        canvas.delete(tag)
    canvas.create_text(cell_side * 2.5,
                       cell_side * 0.5 + cell_side * (5 - size) * 2,
                       text=quantity, fill=draw_color, width=3, tags=tag)
    canvas.create_text(cell_side * 3.5,
                       cell_side * 0.5 + cell_side * (5 - size) * 2,
                       text='x',
                       fill=draw_color,
                       width=3, tags=tag)


def draw_dot(x, y, color, tag):
    canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill=color, tags=tag)


def draw_field(coord_x, coord_y, field, tag, show_placement):
    coord_x = math.ceil(coord_x)
    coord_y = math.ceil(coord_y)

    canvas.create_rectangle(coord_x, coord_y,
                            coord_x + cell_side * 10,
                            coord_y + cell_side * 10,
                            width=3, fill=background_color, outline=draw_color,
                            tags=tag)
    create_grid(coord_x, coord_y,
                coord_x + cell_side * 10,
                coord_y + cell_side * 10, lines_color)
    letters = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'К']
    for ix in range(10):  # draw  numbers and letters
        canvas.create_text(coord_x + cell_side * ix + cell_side / 2,
                           coord_y - cell_side / 2, text=letters[ix],
                           fill=draw_color, tags='coords_' + tag)
        canvas.create_text(coord_x - cell_side / 2,
                           coord_y + cell_side * ix + cell_side / 2,
                           text=ix + 1,
                           fill=draw_color, tags='coords_' + tag)

    list_of_ships = []
    for size in field:
        if size != 'misses':
            list_of_ships.extend(field[size])
    for ship in list_of_ships:
        is_ship_dead = True
        for deck in ship:
            r = deck[0]
            c = deck[1]
            state = deck[2]
            if deck[2] == 0:
                is_ship_dead = False
            if show_placement == True:
                canvas.create_rectangle(coord_x + cell_side * (c - 1),
                                        coord_y + cell_side * (r - 1),
                                        coord_x + cell_side * c,
                                        coord_y + cell_side * r,
                                        width=3, outline=draw_color,
                                        tags='ship_' + tag)
            if state == 1:
                draw_cross(coord_x + cell_side * (c - 1),
                           coord_y + cell_side * (r - 1), 'red', 'cross')
        if is_ship_dead == True:
            draw_borders(ship, coord_x, coord_y, tag)
    for miss in field['misses']:
        r = miss[0]
        c = miss[1]
        draw_dot(coord_x + cell_side * (c - 0.5),
                 coord_y + cell_side * (r - 0.5), 'red', tag + '_misses')


def draw_ship(x, y, size, direction, tag):
    return canvas.create_rectangle(x, y,
                                   x + cell_side + cell_side * (
                                           size - 1) * direction,
                                   y + cell_side + cell_side * (size - 1) * (
                                           1 - direction),
                                   width=3, outline=draw_color,
                                   fill=background_color,
                                   tags=tag)


def draw_new_ship(event_x, event_y, tag):
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


def delete_element(tag):
    canvas.delete(tag)


def delete_elements_inside_rectangle(x1, y1, x2, y2):
    list_of_elements = canvas.find_enclosed(x1 - 3, y1 - 3, x2 + 3, y2 + 3)
    for element in list_of_elements:
        canvas.delete(element)


def init_gui(field, field2):
    global root, canvas
    root = tkinter.Tk()
    root.title('SeaCombat')
    root.iconbitmap('./resources/SeaCombat.ico')
    w = 34 * cell_side
    h = 14 * cell_side
    mw = root.winfo_screenwidth()
    mh = root.winfo_screenheight()
    root.geometry(
        '{}x{}+{}+{}'.format(w, h, (mw - w) // 2, (mh - h) // 2))
    root.resizable(0, 0)

    canvas = tkinter.Canvas(master=root, background=background_color)
    canvas.pack(fill=tkinter.BOTH, expand=True)
    create_grid(0, 0, w, h, lines_color)
    draw_field(field1_left_x, field1_left_y, field, 'player_field', True)
    draw_field(field2_left_x, field2_left_y, field2, 'ai_field', False)
    return root, canvas


def get_checkbox_state():
    return show_enemy_placement.get()


def get_rectangle_coords(tag):
    return canvas.coords(tag)


def move_rect(tag, x, y):
    canvas.move(tag, x, y)


def redraw_field(x, y, field, tag, show_placement):
    coords = get_rectangle_coords(tag)
    delete_elements_inside_rectangle(coords[0] - cell_side,
                                     coords[1] - cell_side, coords[2],
                                     coords[3])
    draw_field(x, y, field, tag, show_placement)


def set_rectangle_coords(tag, x, y, x1, y1):
    canvas.coords(tag, x, y, x1, y1)


def show_battlefield(field):
    for r in range(len(field)):
        for c in range(len(field[r])):
            if field[r][c] == 9:
                field[r][c] = 'o'
            elif field[r][c] == 0:
                field[r][c] = '_'
            else:
                field[r][c] = 'x'
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
