import random


def can_place_ship(row, column, direction, size, field):
    if direction == 1:
        if column + size - 1 > 10: return False
        for x in range(0, size):
            if field[row][column + x] != 0: return False
    elif direction == 0:
        if row + size - 1 > 10: return False
        for x in range(0, size):
            if field[row + x][column] != 0: return False
    return True


def is_ships_placement_legal(field):
    one_deck = 0
    two_deck = 0
    three_deck = 0
    four_deck = 0
    ships = [1, 2, 3, 4]

    for r in field:
        i = 1
        while i < 11:
            if field[r][i] in ships:

                ship_size = field[r][i]
                for s in range(ship_size):
                    if field[r - 1][i + s - 1] in ships:  # check  that there aren't ships on diagonals
                        return False
                    if field[r - 1][i + s + 1] in ships:
                        return False
                    if field[r + 1][i + s - 1] in ships:
                        return False
                    if field[r + 1][i + s + 1] in ships:
                        return False

                    if s + 1 == ship_size:
                        if field[r][i + s + 1] != 9:
                            return False
                        if field[r - 1][i + s] != 9 or field[r + 1][i + s] != 9:
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
                        if field[r - 1][i + s] != 9 or field[r + 1][i + s] != 9:
                            return False
                    elif field[r][i + s + 1] == 9:
                        if field[r - 1][i + s] != ship_size or field[r + 1][i + s] != ship_size:
                            i += 1

    if one_deck > 4 or two_deck > 3 or three_deck > 2 or four_deck > 1:
        return False
    return True


def place_ship(row, column, direction, size, field):
    if direction == 1:
        for r in range(row - 1, row + 2):
            for c in range(column - 1, column + size + 1):
                if r == row and (column - 1 < c and c < column + size):
                    field[r][c] = size
                else:
                    field[r][c] = 9
    elif direction == 0:
        for r in range(row - 1, row + size + 1):
            for c in range(column - 1, column + 1 + 1):
                if (row - 1 < r and r < row + size) and c == column:
                    field[r][c] = size
                else:
                    field[r][c] = 9


def get_blank_field():
    field = [
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
    return field


def get_arranged_ships():
    size = 4
    quantity = 1
    row = 0
    column = 0
    direction = 0

    field = [
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

    while size > 0:
        quantity = 5 - size
        while quantity > 0:
            row = random.randint(1, 10)
            column = random.randint(1, 10)
            if field[row][column] != 0: continue
            direction = random.randint(0, 1)  # 0 - down, 1 - right

            if can_place_ship(row, column, direction, size, field):
                place_ship(row, column, direction, size, field)
                # print("Ship with size " + str(size))
                # show_array()
                quantity = quantity - 1
            elif can_place_ship(row, column, 1 - direction, size, field):
                place_ship(row, column, 1 - direction, size, field)
                # print("Ship with size " + str(size))
                # show_array()
                quantity = quantity - 1
            else:
                continue
        size = size - 1
    return field
