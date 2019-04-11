import math

import seacombat_draw
import seacombat_logic

cell_side = 25
field = None
field2 = None
root = None
canvas = None

def create_ship(event):
    seacombat_draw.draw_new_ship(event.x, event.y, 'new_ship')
    root.bind('<Escape>', delete_ship)
    canvas.tag_bind('new_ship', '<Button-1>', place_ship)
    canvas.tag_bind('new_ship', '<Button-3>', rotate_ship)
    # canvas.tag_bind('new_ship', '<Motion>', move_ship_by_mouse)
    canvas.bind('<Motion>', move_ship_by_mouse)


def delete_ship(event):
    # canvas.tag_unbind('new_ship', '<Motion>')
    canvas.unbind('<Motion>')
    canvas.tag_unbind('new_ship', '<Button-1>')
    canvas.tag_unbind('new_ship', '<Button-3>')
    canvas.delete('new_ship')


def find_array_indexes(coord_x, coord_y):
    field_coords = seacombat_draw.get_rectangle_coords('player_field')
    offset_x = coord_x - field_coords[0]
    offset_y = coord_y - field_coords[1]
    row = offset_y / cell_side
    column = offset_x / cell_side
    return math.ceil(row), math.ceil(column)


def get_ship_tuple_by_coords(event):
    ship_coords = seacombat_draw.get_rectangle_coords('new_ship')
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
    return indexes[0], indexes[1], direction, ship_size


def indicate_legal_state(event):
    if is_placement_legal(event):
        seacombat_draw.change_rectangle_color('new_ship', 'blue')
    else:
        seacombat_draw.change_rectangle_color('new_ship', 'red')


def move_ship_by_mouse(event):
    indicate_legal_state(event)
    ship = seacombat_draw.get_rectangle_coords('new_ship')
    ship_x = (ship[2] - ship[0]) / 2
    ship_y = (ship[3] - ship[1]) / 2
    seacombat_draw.move_rect('new_ship', event.x - ship[0] - ship_x,
                             event.y - ship[1] - ship_y)


def is_placement_legal(event):
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
        field_coords = seacombat_draw.get_rectangle_coords('player_field')
        seacombat_draw.redraw_field(field_coords[0], field_coords[1], field, 'player_field')


def rotate_ship(event):
    ship_coords = seacombat_draw.get_rectangle_coords('new_ship')
    left_x = ship_coords[0]
    top_y = ship_coords[1]
    right_x = ship_coords[2]
    down_y = ship_coords[3]

    central_point_x = (right_x - left_x) / 2
    central_point_y = (down_y - top_y) / 2
    seacombat_draw.set_rectangle_coords('new_ship',
                                        ship_coords[0] + central_point_x - central_point_y,
                                        ship_coords[1] - central_point_x + central_point_y,
                                        ship_coords[2] - central_point_x + central_point_y,
                                        ship_coords[3] + central_point_x - central_point_y)

    indicate_legal_state(event)


def start(f1, f2):
    try:
        global field, field2, root, canvas
        field = f1
        field2 = f2
        root, canvas = seacombat_draw.init_gui(field, field2)

        tag = seacombat_draw.draw_list_of_ships()
        canvas.tag_bind(tag, '<Button-1>', create_ship)
        root.mainloop()
    except Exception as e:
        print(e)
