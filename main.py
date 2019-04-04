import random

size = 4
quantity = 0
row = 0
column = 0
direction = 0
field = [
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
    [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
    [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
    [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
    [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
    [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
    [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
    [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
    [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
    [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
]


def can_place_ship(row, column, direction, size, field):
    if row + size - 1 > 10 or column + size - 1 > 10: return False

    if direction == 1:
        for x in range(0, size - 1):
            if field[row + x][column] != 0: return False

    if direction == 0:
        for x in range(0, size - 1):
            if field[row][column + x] != 0: return False

    return True


def place_ship(row, column, direction, size, field):
    if direction == 1:
        for y in range(row - 1, row + 1):
            for x in range(column - 1, column + size):
                if y == row and column < x < column + size:
                    field[y][x] = size
                else:
                    field[y][x] = -1
    elif direction == 0:
        for y in range(row - 1, row + size):
            for x in range(column - 1, column + 1):
                if row < y < row + size and x == column:
                    field[y][x] = size
                else:
                    field[y][x] = -1


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
            print("Ship was placed with size " + str(size))
            quantity = quantity - 1
        elif can_place_ship(row, column, 1 - direction, size, field):
            # placeship
            place_ship(row, column, 1 - direction, size, field)
            print("Ship was placed with size " + str(size))
            quantity = quantity - 1
        else:
            continue
    size = size - 1

print("a=", field)
print("Hello world!")
print("Ship size equals to " + str(size))
