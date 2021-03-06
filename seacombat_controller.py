import math
import random

import seacombat_draw
import seacombat_logic

cell_side = 25
field = None
field2 = None
root = None
canvas = None
path_to_save_file = './resources/save_test.json'


def create_ship(event):
    seacombat_draw.draw_new_ship(event.x, event.y, 'new_ship')
    root.bind('<Escape>', delete_ship)
    canvas.tag_bind('new_ship', '<Button-1>', place_ship)
    canvas.tag_bind('new_ship', '<Button-3>', rotate_ship)
    # canvas.tag_bind('new_ship', '<Motion>', move_ship_by_mouse)
    canvas.bind('<Motion>', move_ship_by_mouse)


def draw_list_of_ships(field):
    size = 4
    while size > 0:
        ship_tag = 'ship' + str(size)
        quantity = 5 - size - len(field[size])
        seacombat_draw.draw_counter_of_ship('ship_counter_' + str(size), size,
                                            quantity)

        left_x = cell_side * 4
        left_y = 2 * cell_side * (5 - size)

        if len(seacombat_draw.get_rectangle_coords(ship_tag)) <= 0:
            seacombat_draw.draw_ship(left_x, left_y, size, 1, ship_tag)

        if quantity > 0:
            canvas.tag_bind(ship_tag, '<Button-1>', create_ship)
        else:
            canvas.tag_unbind(ship_tag, '<Button-1>')
        size -= 1


def delete_ship(event):
    canvas.unbind('<Motion>')
    canvas.tag_unbind('new_ship', '<Button-1>')
    canvas.tag_unbind('new_ship', '<Button-3>')
    canvas.delete('new_ship')


def find_array_indexes(coord_x, coord_y, field_tag):
    field_coords = seacombat_draw.get_rectangle_coords(field_tag)
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
                                     event.y, 'player_field')
    else:
        indexes = find_array_indexes(event.x,
                                     top_y + cell_side / 2, 'player_field')
    return indexes[0], indexes[1], direction, ship_size


def save_game_state():
    seacombat_logic.save_to_file(path_to_save_file, field, field2)
    print('Game saved.')


def load_game_state():
    global field, field2
    fields = seacombat_logic.load_from_file(path_to_save_file)
    field = fields[0]
    field2 = fields[1]
    redraw_player_field()
    redraw_enemy_field()
    draw_list_of_ships(field)
    if seacombat_logic.is_ships_placement_legal(field) and \
            seacombat_logic.are_all_ships_dead(field) == False:
        canvas.tag_bind('player_field', '<Button-1>', shot_at_left_field)
    else:
        canvas.tag_unbind('player_field', '<Button-1>')

    if seacombat_logic.is_ships_placement_legal(field2) and \
            seacombat_logic.are_all_ships_dead(field2) == False:
        canvas.tag_bind('ai_field', '<Button-1>', shot_at_right_field)
    else:
        canvas.tag_unbind('ai_field', '<Button-1>')
    print('Game loaded.')


def shot_at_left_field(event):
    shot_at_field(event, field, 'player_field', True)


def shot_at_right_field(event):
    shot_at_field(event, field2, 'ai_field',
                  seacombat_draw.get_checkbox_state())



def ai_shot_at_field(field, field_tag):
    reset_ai_field()
    shot_count = 0
    list = []
    while (seacombat_logic.are_all_ships_dead(field) != True):
        x, y = seacombat_logic.get_next_shot()
        if (x, y) in list:
            continue
        list.append((x, y))
        shot_count += 1
        seacombat_logic.result_of_shooting(x, y, field)
        field_coords = seacombat_draw.get_rectangle_coords(field_tag)
        seacombat_draw.redraw_field(field_coords[0], field_coords[1], field,
                                    field_tag, True)
        root.update_idletasks()
        # time.sleep(0.01)
    print(str(shot_count))


def shot_at_field(event, field, field_tag, show_placement):
    target_cell = find_array_indexes(event.x, event.y, field_tag)
    if target_cell[0] > 10 or target_cell[1] > 10 or target_cell[0] <= 0 or \
            target_cell[1] <= 0:
        return
    if len(seacombat_draw.get_rectangle_coords('new_ship')) != 0:
        return
    result = seacombat_logic.result_of_shooting(target_cell[0], target_cell[1],
                                                field)
    field_coords = seacombat_draw.get_rectangle_coords(field_tag)
    seacombat_draw.redraw_field(field_coords[0], field_coords[1], field,
                                field_tag, show_placement)
    if seacombat_logic.are_all_ships_dead(field):
        canvas.tag_unbind(field_tag, '<Button-1>')
        canvas.create_text(25 * cell_side,
                           cell_side / 2, text="All ships are dead",
                           fill='red', tags='message')


def ai_shooting(field):
    pass


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
    if seacombat_logic.can_place_ship(row=ship[0], column=ship[1],
                                      direction=ship[2], size=ship[3],
                                      field=field):
        return True
    else:
        return False


def place_ship(event):
    ship = get_ship_tuple_by_coords(event)
    if seacombat_logic.can_place_ship(row=ship[0], column=ship[1],
                                      direction=ship[2], size=ship[3],
                                      field=field):
        field[ship[3]].append(
            seacombat_logic.get_ship(ship[0], ship[1], ship[2], ship[3]))
        delete_ship(event)
        field_coords = seacombat_draw.get_rectangle_coords('player_field')
        seacombat_draw.redraw_field(field_coords[0], field_coords[1], field,
                                    'player_field', True)
        draw_list_of_ships(field)
    if seacombat_logic.is_ships_placement_legal(field):
        canvas.tag_bind('player_field', '<Button-1>', shot_at_left_field)
    else:
        canvas.tag_unbind('player_field', '<Button-1>')


def redraw_enemy_field():
    field_coords = seacombat_draw.get_rectangle_coords('ai_field')
    seacombat_draw.delete_element('message')
    seacombat_draw.redraw_field(field_coords[0], field_coords[1], field2,
                                'ai_field',
                                show_placement=seacombat_draw.get_checkbox_state())


def redraw_player_field():
    field_coords = seacombat_draw.get_rectangle_coords('player_field')
    seacombat_draw.delete_element('message')
    seacombat_draw.redraw_field(field_coords[0], field_coords[1], field,
                                'player_field',
                                show_placement=True)


def rotate_ship(event):
    ship_coords = seacombat_draw.get_rectangle_coords('new_ship')
    left_x = ship_coords[0]
    top_y = ship_coords[1]
    right_x = ship_coords[2]
    down_y = ship_coords[3]

    central_point_x = (right_x - left_x) / 2
    central_point_y = (down_y - top_y) / 2
    seacombat_draw.set_rectangle_coords('new_ship',
                                        left_x + central_point_x - central_point_y,
                                        top_y - central_point_x + central_point_y,
                                        right_x - central_point_x + central_point_y,
                                        down_y + central_point_x - central_point_y)
    indicate_legal_state(event)


def reset_player_field():
    global field
    field = seacombat_logic.get_blank_field()
    field_coords = seacombat_draw.get_rectangle_coords('player_field')
    seacombat_draw.redraw_field(field_coords[0], field_coords[1], field,
                                'player_field', True)
    draw_list_of_ships(field)
    canvas.tag_unbind('player_field', '<Button-1>')


def reset_ai_field():
    global field2
    field2 = seacombat_logic.reset_field_state(field2)
    field_coords = seacombat_draw.get_rectangle_coords('ai_field')
    seacombat_draw.redraw_field(field_coords[0], field_coords[1], field2,
                                'ai_field', True)
    canvas.tag_bind('ai_field', '<Button-1>', shot_at_right_field)
    checkbox.invoke()
    checkbox.invoke()


def start(f1, f2):
    try:
        global field, field2, root, canvas
        field = f1
        field2 = f2

        root, canvas = seacombat_draw.init_gui()
        seacombat_draw.draw_fields(field, field2)
        draw_list_of_ships(field)
        seacombat_draw.create_menu(save_game_state, load_game_state)

        seacombat_draw.draw_button(cell_side * 2, cell_side * 10, cell_side,
                                   cell_side * 3,
                                   'Reset L',
                                   reset_player_field)
        seacombat_draw.draw_button(cell_side * 6, cell_side * 10, cell_side,
                                   cell_side * 3,
                                   'Reset R',
                                   lambda: reset_ai_field())
        global checkbox
        checkbox = seacombat_draw.create_checkbox_for_enemy_field(2 * cell_side,
                                                                  12 * cell_side,
                                                                  redraw_enemy_field)
        canvas.tag_bind('player_field', '<Button-1>', shot_at_left_field)
        canvas.tag_bind('ai_field', '<Button-1>', shot_at_right_field)
        seacombat_draw.draw_button(cell_side * 26, cell_side * 12, cell_side,
                                   cell_side * 3,
                                   'AI_Shooting',
                                   lambda: ai_shot_at_field(field2, "ai_field"))
        root.mainloop()
    except Exception as e:
        print(e)
