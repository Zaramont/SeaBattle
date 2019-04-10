import seacombat_draw
import math
import seacombat_logic
cell_side = 25
field = None
field2 = None

def create_ship(event):

    seacombat_draw.create_rectangle(event.x,event.y,'new_ship')
    # root.bind('<Escape>', delete_ship)
    canvas.bind('<Button-1>', place_ship)
    canvas.bind('<Button-3>', rotate_ship)
    canvas.bind('<Motion>', move_ship_by_mouse)
    # canvas.bind('<Button-1>', indicate_legal_state) # for test


def delete_ship(event):
    canvas.unbind('<Motion>')
    canvas.unbind('<Button-1>')
    canvas.unbind('<Button-3>')
    canvas.delete('new_ship')


def find_array_indexes(coord_x, coord_y):
    field_coords = canvas.coords('player_field')
    offset_x = coord_x - field_coords[0]
    offset_y = coord_y - field_coords[1]
    row = offset_y / cell_side
    column = offset_x / cell_side
    return math.ceil(row), math.ceil(column)
    # print("row= {} column= {}".format(row, column))


def get_rect_coords(tag):
    return canvas.coords(tag)


def get_ship_tuple_by_coords(event):
    field_coords = get_rect_coords('player_field')
    ship_coords = get_rect_coords('new_ship')
    left_x = ship_coords[0]
    top_y = ship_coords[1]
    right_x = ship_coords[2]
    down_y = ship_coords[3]
    if right_x - left_x > down_y - top_y:
        direction = 1
        ship_size = int((right_x - left_x) / cell_side)
    else:
        direction = 0
        ship_size = int((down_y - top_y) / cell_side)

    if direction == 1:
        indexes = find_array_indexes(left_x + cell_side / 2,
                                     event.y)
    else:
        indexes = find_array_indexes(event.x,
                                     top_y + cell_side / 2)
    return (indexes[0], indexes[1], direction, ship_size)


def indicate_legal_state(event):
    if placement_legal(event):
        elem = canvas.find_withtag('new_ship')[0]
        canvas.itemconfig(elem, outline='blue')
    else:
        elem = canvas.find_withtag('new_ship')[0]
        canvas.itemconfig(elem, outline='red')
    # canvas.create_rectangle(event.x, event.y, event.x + 3 * cell_side, event.y + cell_side)


def move_ship_by_mouse(event):
    indicate_legal_state(event)
    ship = canvas.coords('new_ship')
    ship_x = (ship[2] - ship[0]) / 2
    ship_y = (ship[3] - ship[1]) / 2
    canvas.move('new_ship', event.x - ship[0] - ship_x,
                event.y - ship[1] - ship_y)


def placement_legal(event):
    ship = get_ship_tuple_by_coords(event)
    if seacombat_logic.can_place_ship(ship[0], ship[1], ship[2], ship[3],
                                      field):
        return True
    else:
        return False


def place_ship(event):
    ship = get_ship_tuple_by_coords(event)
    if seacombat_logic.can_place_ship(ship[0], ship[1], ship[2], ship[3],
                                      field):
        field[ship[3]].append(
            seacombat_logic.get_ship(ship[0], ship[1], ship[2], ship[3]))
        delete_ship(event)
        redraw_field(field1_left_x, field1_left_y, field, 'player_field')


def rotate_ship(event):
    ship_coords = canvas.coords('new_ship')
    left_x = ship_coords[0]
    top_y = ship_coords[1]
    right_x = ship_coords[2]
    down_y = ship_coords[3]

    central_point_x = (right_x - left_x) / 2
    central_point_y = (down_y - top_y) / 2
    canvas.coords('new_ship',
                  ship_coords[0] + central_point_x - central_point_y,
                  ship_coords[1] - central_point_x + central_point_y,
                  ship_coords[2] - central_point_x + central_point_y,
                  ship_coords[3] + central_point_x - central_point_y)

    indicate_legal_state(event)


canvas = seacombat_draw.init_gui()
ships = seacombat_draw.draw_list_of_ships()
for x in ships:
    canvas.tag_bind('ship', '<Button-1>', create_ship)