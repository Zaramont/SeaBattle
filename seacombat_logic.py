import random


def are_ships_crossed(ship1, ship2):
    ship1_set = get_ship_with_area_around(ship1)
    ship2_set = get_ship_with_area_around(ship2)
    common_set = ship1_set & ship2_set
    if len(common_set) > 0:
        if len(ship1 & common_set) > 0 or len(ship2 & common_set) > 0:
            return True
    return False


def can_place_ship(row, column, direction, size, field):
    list_of_ships = []
    ship1 = get_ship(row, column, direction, size)

    wrong_decks = [deck for deck in ship1 if
                   deck[0] > 10 or deck[0] < 1 or deck[1] > 10 or deck[1] < 1]
    if len(wrong_decks) > 0 or len(field[size]) == 5 - size:
        return False

    for i in field:
        list_of_ships.extend(field[i])

    for ship2 in list_of_ships:
        if are_ships_crossed(ship1, ship2):
            return False

    return True


def is_ships_placement_legal(field):
    list_of_ships = []

    for size in field:
        if len(field[size]) == (5 - size):
            list_of_ships.extend(field[size])
        else:
            return False
    for ship in list_of_ships:
        wrong_decks = [deck for deck in ship if
                       deck[0] > 10 or deck[0] < 1 or
                       deck[1] > 10 or deck[1] < 1
                       ]
        if len(wrong_decks) > 0:
            return False

    quantity = len(list_of_ships)
    for ix in range(quantity - 1):
        for iy in (ix + 1, quantity):
            if are_ships_crossed(list_of_ships[ix], list_of_ships[iy]):
                return False
    return True


def get_arranged_ships():
    size = 4
    field = get_blank_field()

    while size > 0:
        quantity = 5 - size
        while quantity > 0:
            row = random.randint(1, 10)
            column = random.randint(1, 10)
            direction = random.randint(0, 1)  # 0 - vertical, 1 - horizontal

            if can_place_ship(row, column, direction, size, field):
                place_ship(row, column, direction, size, field)
                quantity = quantity - 1
            elif can_place_ship(row, column, 1 - direction, size, field):
                place_ship(row, column, 1 - direction, size, field)
                quantity = quantity - 1
            else:
                continue
        size = size - 1
    return field


def get_blank_field():
    field = {1: [], 2: [], 3: [], 4: [], 'misses': set()}
    # field = {1: [{(3, 6, 1)}, {(5, 9, 0)}, {(3, 4, 0)}, {(1, 3, 0)}], 2: [{(7, 10, 0), (7, 9, 1)}, {(7, 4, 1), (7, 5, 0)}, {(10, 7, 0), (9, 7, 0)}], 3: [{(1, 9, 1), (3, 9, 0), (2, 9, 0)}, {(10, 4, 0), (10, 3, 0), (10, 2, 0)}], 4: [{(5, 4, 0), (5, 1, 0), (5, 2, 0), (5, 3, 0)}]}
    return field


def get_test_field():
    field = {
        1: [{(3, 6, 1)}, {(5, 9, 0)}, {(3, 4, 0)}, {(1, 3, 0)}],
        2: [{(7, 10, 0), (7, 9, 1)}, {(7, 4, 1), (7, 5, 0)}, {(10, 7, 0), (9, 7, 0)}],
        3: [{(1, 9, 1), (3, 9, 0), (2, 9, 0)}, {(10, 4, 0), (10, 3, 0), (10, 2, 0)}],
        4: [{(5, 4, 0), (5, 1, 0), (5, 2, 0), (5, 3, 0)}],
        'misses': {(1, 1), (1, 2), (1, 4)}
    }
    return field


def get_ship(row, column, direction, size):
    coord_set = set()
    if direction == 1:
        for n in range(size):
            deck = row, column + n, 0
            coord_set.add(deck)
    elif direction == 0:
        for n in range(size):
            deck = row + n, column, 0
            coord_set.add(deck)
    return coord_set


def get_ship_with_area_around(ship):
    surrounded_ship = set()
    for deck in ship:
        temp_set = set()
        for r in range(deck[0] - 1, deck[0] + 2):
            for c in range(deck[1] - 1, deck[1] + 2):
                temp_set.add((r, c, 0))
        surrounded_ship = surrounded_ship | temp_set
    return surrounded_ship


def place_ship(row, column, direction, size, field):
    ship = get_ship(row, column, direction, size)
    field[size].append(ship)


def result_of_shooting(row, column, field):
    # target_ship = None
    # list_of_ships = []
    for size in field:  # draw ships on field
        if size != 'misses':
            for ship in field[size]:
                if (row,column,0) in ship:
                    ship.add((row,column,1))
                    ship.discard((row,column,0))
                    for deck in ship:
                        if deck[2]==0:
                            return 'HIT !!!'
                    misses = get_ship_with_area_around(ship)
                    for miss in misses:
                        if (miss[0],miss[1],0) not in ship and (miss[0],miss[1],1) not in ship and (miss[0]>0 and miss[0]<11) and ((miss[1]>0 and miss[1]<11)):
                            field['misses'].add((miss[0],miss[1]))
                    return 'KILL !!!'
                elif (row,column,1) in ship:
                    return
    field['misses'].add((row,column))
    return 'MISS !!!'
