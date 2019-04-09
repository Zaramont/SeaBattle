import copy
import math
import tkinter

import seacombat_logic

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


def create_ship(event):
    if canvas.coords('new_ship'):  # prevent creation of two new ships
        return

    ship = canvas.find_closest(event.x, event.y)
    ship_coords = canvas.coords(ship)
    ship_size = (ship_coords[2] - ship_coords[0]) / cell_side

    width = cell_side * ship_size
    x = event.x - width / 2
    y = event.y - cell_side / 2
    canvas.create_rectangle(x, y,
                            x + cell_side * ship_size,
                            y + cell_side, width=3, outline=draw_color,
                            tags='new_ship')
    root.bind('<Escape>', delete_ship)
    canvas.bind('<Button-1>', place_ship)
    canvas.bind('<Button-3>', rotate_ship)
    canvas.bind('<Motion>', move_ship_by_mouse)
    # canvas.bind('<Button-1>', indicate_legal_state) # for test


def delete_ship(event):
    canvas.unbind('<Motion>')
    canvas.unbind('<Button-1>')
    canvas.unbind('<Button-3>')
    canvas.delete('new_ship')


def draw_list_of_ships():
    size = 4
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
        canvas.create_rectangle(left_x, left_y, left_x + cell_side * size,
                                left_y + cell_side,
                                width=3, outline=draw_color,
                                fill=background_color,
                                tags='ship' + str(size))
        canvas.tag_bind('ship' + str(size), '<Button-1>', create_ship)
        # lambda event: create_ship(event, size))
        # canvas.update()
        size -= 1


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

    for r in range(1, 11):
        for c in range(1, 11):
            if field[r][c] in [1, 2, 3, 4]:  # remember this bug)
                # print("c= " + str(c) + " r= " + str(r))
                canvas.create_rectangle(coord_x + cell_side * (c - 1),
                                        coord_y + cell_side * (r - 1),
                                        coord_x + cell_side * c,
                                        coord_y + cell_side * r,
                                        width=3, outline=draw_color)


def find_array_indexes(coord_x, coord_y):
    field_coords = canvas.coords('player_field')
    offset_x = coord_x - field_coords[0]
    offset_y = coord_y - field_coords[1]
    row = offset_y / cell_side
    column = offset_x / cell_side
    return math.ceil(row), math.ceil(column)
    # print("row= {} column= {}".format(row, column))


def indicate_legal_state(event):
    if placement_legal(event):
        elem = canvas.find_withtag('new_ship')[0]
        canvas.itemconfig(elem, outline='blue')
    else:
        elem = canvas.find_withtag('new_ship')[0]
        canvas.itemconfig(elem, outline='red')
    # canvas.create_rectangle(event.x, event.y, event.x + 3 * cell_side, event.y + cell_side)


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


def move_ship_by_mouse(event):
    indicate_legal_state(event)
    ship = canvas.coords('new_ship')
    ship_x = (ship[2] - ship[0]) / 2
    ship_y = (ship[3] - ship[1]) / 2
    canvas.move('new_ship', event.x - ship[0] - ship_x,
                event.y - ship[1] - ship_y)


def placement_legal(event):
    global field3
    field3 = copy.deepcopy(field)

    field_coords = canvas.coords('player_field')
    ship_coords = canvas.coords('new_ship')
    left_x = ship_coords[0]
    top_y = ship_coords[1]
    right_x = ship_coords[2]
    down_y = ship_coords[3]

    if left_x + cell_side / 2 < field_coords[0] or right_x - cell_side / 2 > field_coords[2]:
        return False
    elif top_y + cell_side / 2 < field_coords[1] or down_y - cell_side / 2 > field_coords[3]:
        return False

    # direction 1-horizontal, 0 - vertical
    if right_x - left_x > down_y - top_y:
        direction = 1
        ship_size = int((right_x - left_x) / cell_side)
    else:
        direction = 0
        ship_size = int((down_y - top_y) / cell_side)

    for n in range(ship_size):
        if direction == 1:
            indexes = find_array_indexes(left_x + n * cell_side + cell_side / 2, event.y)
            if indexes[0] > 10 or indexes[1] > 10:
                return False
            if field3[indexes[0]][indexes[1]] in [1, 2, 3, 4]:
                return False
            field3[indexes[0]][indexes[1]] = ship_size
            # array.append(indexes[0])
            # array.append(indexes[1])
        else:
            indexes = find_array_indexes(event.x, top_y + n * cell_side + cell_side / 2)

            if field3[indexes[0]][indexes[1]] in [1, 2, 3, 4]:
                return False
            field3[indexes[0]][indexes[1]] = ship_size
    if seacombat_logic.is_ships_placement_legal(field3):
        return True
    else:
        return False


def place_ship(event):
    if placement_legal(event):
        global field
        field = field3
        delete_ship(event)
        redraw_field(field1_left_x, field1_left_y, field, 'player_field')


def redraw_field(x, y, field3, tag):
    draw_field(x, y, field3, tag)


def rotate_ship(event):
    ship_coords = canvas.coords('new_ship')
    left_x = ship_coords[0]
    top_y = ship_coords[1]
    right_x = ship_coords[2]
    down_y = ship_coords[3]

    central_point_x = (right_x - left_x) / 2
    central_point_y = (down_y - top_y) / 2
    canvas.coords('new_ship', ship_coords[0] + central_point_x - central_point_y,
                  ship_coords[1] - central_point_x + central_point_y , ship_coords[2] - central_point_x + central_point_y,
                  ship_coords[3] + central_point_x - central_point_y )

    indicate_legal_state(event)


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
    for r in field:
        print(r)
