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

    while (size > 0):
        quantity = 5 - size
        while (quantity > 0):
            row = random.randint(1, 10)
            column = random.randint(1, 10)
            if field[row][column] != 0: continue
            direction = random.randint(0, 1)  # 0 - down, 1 - right

            if can_place_ship(row, column, direction, size, field):
                # placeship
                place_ship(row, column, direction, size, field)
                # print("Ship with size " + str(size))
                # show_array()
                quantity = quantity - 1
            elif can_place_ship(row, column, 1 - direction, size, field):
                # placeship
                place_ship(row, column, 1 - direction, size, field)
                # print("Ship with size " + str(size))
                # show_array()
                quantity = quantity - 1
            else:
                continue
        size = size - 1
    return field
