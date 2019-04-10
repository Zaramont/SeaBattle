import random
import seacombat_draw

def can_place_ship(row, column, direction, size, field):
    list_of_ships = []
    ship1 = get_ship(row, column, direction, size)
    wrong_decks = [deck for deck in ship1 if deck[0] > 10 or deck[0] < 1 or deck[1] > 10 or deck[1] < 1]

    if len(wrong_decks) > 0:
        return False

    for i in field:
        list_of_ships.extend(field[i])

    for ship2 in list_of_ships:
        if are_ships_touched(ship1, ship2):
            return False

    return True


def are_ships_touched(ship1, ship2):
    ship1_set = get_ship_with_area_around(ship1)
    ship2_set = get_ship_with_area_around(ship2)
    common_set = ship1_set & ship2_set
    if len(common_set) > 0:
        if len(ship1 & common_set)>0 or len(ship2 & common_set)>0:
            return True
    return False


def is_ships_placement_legal(field):
    one_deck = 0
    two_deck = 0
    three_deck = 0
    four_deck = 0

    for r in range(1, 11):
        i = 1
        while i < 11:
            if field[r][i] in [1, 2, 3, 4]:

                ship_size = field[r][i]
                for s in range(ship_size):
                    if field[r - 1][i + s - 1] not in [0, 9]:  # check  that there aren't ships on diagonals
                        return False
                    if field[r - 1][i + s + 1] not in [0, 9]:
                        return False
                    if field[r + 1][i + s - 1] not in [0, 9]:
                        return False
                    if field[r + 1][i + s + 1] not in [0, 9]:
                        return False

                    if s + 1 == ship_size:  # if last part of ship or ship with one deck
                        if field[r][i + s + 1] not in [0, 9]:  # check next point
                            return False
                        if field[r - 1][i + s] not in [0, 9] or field[r + 1][i + s] not in [0,
                                                                                            9]:  # check points up and down
                            return False
                        i = i + ship_size

                        if ship_size == 1:
                            one_deck += 1
                        elif ship_size == 2:
                            two_deck += 1
                        elif ship_size == 3:
                            three_deck += 1
                        elif ship_size == 4:
                            four_deck += 1
                        continue

                    if field[r][i + s + 1] == ship_size:
                        if field[r - 1][i + s] not in [0, 9] or field[r + 1][i + s] not in [0, 9]:
                            return False
                    elif field[r][i + s + 1] in [0, 9]:
                        if field[r + 1][i + s] == ship_size and field[r - 1][i + s] in [0, 9]:
                            for ix in range(1, ship_size):
                                if ix + 1 == ship_size:
                                    if field[r + ix + 1][i + s] in [0, 9]:
                                        if ship_size == 1:
                                            one_deck += 1
                                        elif ship_size == 2:
                                            two_deck += 1
                                        elif ship_size == 3:
                                            three_deck += 1
                                        elif ship_size == 4:
                                            four_deck += 1
                                        break
                                elif field[r + ix + 1][i + s] == ship_size:
                                    continue
                                return False
                            i += 1
                            break
                        elif field[r - 1][i + s] == ship_size:
                            i += 1
                            break
            elif field[r][i] not in [0, 9]:
                return False
            else:
                i += 1
    if one_deck > 4 or two_deck > 3 or three_deck > 2 or four_deck > 1:
        return False
    return True


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
    # seacombat_draw.show_dict_field(field)

def get_blank_field():
    field = {1: [], 2: [], 3: [], 4: []}
    return field


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
