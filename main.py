import random

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

def show_battlefield():
    for r in range(len(field)):
        for c in range(len(field[r])):
            if field[r][c] == 9:
                field[r][c] = 'o'
            elif field[r][c] == 0:
                field[r][c] = "_"
            else:
                field[r][c] = "x"
    show_array()

def show_array():
    for r in field:
        print(r)

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
        for y in range(row - 1, row + 2):
            for x in range(column - 1, column + size + 1):
                if y == row and (column - 1 < x and x < column + size):
                    field[y][x] = size
                else:
                    field[y][x] = 9
    elif direction == 0:
        for y in range(row - 1, row + size + 1):
            for x in range(column - 1, column + 2):
                if (row - 1 < y and y < row + size) and x == column:
                    field[y][x] = size
                else:
                    field[y][x] = 9

while (size > 0):
    quantity = 5 - size
    while (quantity > 0):
        row = random.randint(1, 10);
        column = random.randint(1, 10)
        # if field[row,column] != 0: continue
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

show_battlefield()
