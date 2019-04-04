import random

import seacombat_logic

seacombat_logic.arrange_ships()
field = seacombat_logic.field


def shot_to_point(row, column):
    value = field[row][column]
    if (value == 9) or (value == 0):
        return "miss"
    elif value == 1:
        field[row][column] = 'x'  # value * 10
        return "kill"
    elif value in [2, 3, 4]:
        field[row][column] = 'x'  # value * 10
        return "hit"


for x in range(16):
    row = random.randint(1, 10)
    column = random.randint(1, 10)
    print("Shot at point " + str(row) + ' ' + str(column),
          shot_to_point(row, column))
