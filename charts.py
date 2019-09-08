import random

import pandas as pd
from matplotlib import pyplot as plt

import seacombat_logic


def alg1(field):
    field = seacombat_logic.reset_field_state(field)
    shot_count = 0
    previous_shots = []
    x, y = seacombat_logic.get_random_shot()
    while (seacombat_logic.are_all_ships_dead(field) != True):
        while (x, y) in previous_shots:
            x, y = seacombat_logic.get_random_shot()
        previous_shots.append((x, y))
        shot_count += 1
        seacombat_logic.result_of_shooting(x, y, field)
    return shot_count


def alg2(field):
    field = seacombat_logic.reset_field_state(field)

    shot_count = 0
    last_shot = None
    last_result = None
    value_shots = []
    previous_shots = set()
    wounded_ship = []
    killing_mode = False

    while (seacombat_logic.are_all_ships_dead(field) != True):
        if killing_mode == False:
            if last_result == 'KILL':
                sur_arr = seacombat_logic.get_ship_with_area_around(
                    {(last_shot)})
                for deck in sur_arr:
                    previous_shots.add((deck[0], deck[1]))
            elif last_result == 'HIT':
                killing_mode = True
                wounded_ship.append(last_shot)
                last_r = last_shot[0]
                last_c = last_shot[1]
                coords = ((last_r - 1, last_c), (last_r + 1, last_c),
                          (last_r, last_c - 1), (last_r, last_c + 1))
                for r, c in coords:
                    if (r, c) not in previous_shots:
                        value_shots.append((r, c))

        elif killing_mode == True:
            if last_result == 'KILL':
                wounded_ship.append(last_shot)
                sur_arr = seacombat_logic.get_ship_with_area_around(
                    set(wounded_ship))
                for deck in sur_arr:
                    previous_shots.add((deck[0], deck[1]))
                wounded_ship = []
                killing_mode = False
            elif last_result == 'HIT':
                wounded_ship.append(last_shot)
                value_shots = []
                coords = []
                if wounded_ship[0][0] == wounded_ship[1][0]:
                    for deck in wounded_ship:
                        coords.append((deck[0], deck[1] - 1))
                        coords.append((deck[0], deck[1] + 1))
                else:
                    for deck in wounded_ship:
                        coords.append((deck[0] - 1, deck[1]))
                        coords.append((deck[0] + 1, deck[1]))
                for r, c in coords:
                    if (r, c) not in previous_shots:
                        value_shots.append((r, c))

        if killing_mode == False:
            last_shot = seacombat_logic.get_random_shot()
            while last_shot in previous_shots:
                last_shot = seacombat_logic.get_random_shot()
        else:
            last_shot = value_shots.pop(
                random.randint(0, len(value_shots) - 1))

        previous_shots.add(last_shot)
        shot_count += 1
        last_result = seacombat_logic.result_of_shooting(last_shot[0],
                                                         last_shot[1], field)
    return shot_count


def alg3(field):
    field = seacombat_logic.reset_field_state(field)
    shot_count = 0
    last_shot = None
    last_result = None
    value_shots = []
    previous_shots_set = set()
    wounded_ship = []
    killing_mode = False

    ships = {1: 4, 2: 3, 3: 2, 4: 1}
    shots_set = get_four_deck_shots()

    while (seacombat_logic.are_all_ships_dead(field) != True):
        if killing_mode == False:
            if last_result == 'KILL':
                sur_arr = seacombat_logic.get_ship_with_area_around(
                    {(last_shot)})
                for deck in sur_arr:
                    previous_shots_set.add((deck[0], deck[1]))
                ships[1] -= 1
            elif last_result == 'HIT':
                killing_mode = True
                wounded_ship.append(last_shot)
                last_r = last_shot[0]
                last_c = last_shot[1]
                coords = ((last_r - 1, last_c), (last_r + 1, last_c),
                          (last_r, last_c - 1), (last_r, last_c + 1))
                for r, c in coords:
                    if (r, c) not in previous_shots_set:
                        value_shots.append((r, c))

        elif killing_mode == True:
            if last_result == 'KILL':
                wounded_ship.append(last_shot)
                sur_arr = seacombat_logic.get_ship_with_area_around(
                    set(wounded_ship))
                for deck in sur_arr:
                    previous_shots_set.add((deck[0], deck[1]))
                if len(wounded_ship) == 4:
                    shots_set = shots_set.union(get_three_two_deck_shots())
                ships[len(wounded_ship)] -= 1
                wounded_ship = []
                killing_mode = False
            elif last_result == 'HIT':
                wounded_ship.append(last_shot)
                value_shots = []
                coords = []
                if wounded_ship[0][0] == wounded_ship[1][0]:
                    for deck in wounded_ship:
                        coords.append((deck[0], deck[1] - 1))
                        coords.append((deck[0], deck[1] + 1))
                else:
                    for deck in wounded_ship:
                        coords.append((deck[0] - 1, deck[1]))
                        coords.append((deck[0] + 1, deck[1]))
                for r, c in coords:
                    if (r, c) not in previous_shots_set:
                        value_shots.append((r, c))

        if killing_mode == False:
            # if ships[2] == 0 and ships[3] == 0 and ships[4] == 0:
            #     shots_set = set()
            # else:
            shots_set = shots_set.difference(previous_shots_set)
            if len(shots_set) == 0:
                last_shot = seacombat_logic.get_random_shot()
                while last_shot in previous_shots_set:
                    last_shot = seacombat_logic.get_random_shot()
            else:
                last_shot = shots_set.pop()
        else:
            last_shot = value_shots.pop(
                random.randint(0, len(value_shots) - 1))

        previous_shots_set.add(last_shot)
        shot_count += 1
        last_result = seacombat_logic.result_of_shooting(last_shot[0],
                                                         last_shot[1], field)
    return shot_count


def get_three_two_deck_shots():
    shots_set = set()
    coords = [(1, 1), (5, 1), (9, 1), (1, 5), (1, 9)]
    for r, c in coords:

        while c < 11 and r < 11:
            shots_set.add((r, c))
            r += 1
            c += 1
    return shots_set

def get_four_deck_shots():
    shots_set = set()
    coords = [(3, 1), (7, 1), (1, 3), (1, 7)]
    for r, c in coords:

        while c < 11 and r < 11:
            shots_set.add((r, c))
            r += 1
            c += 1
    return shots_set


list_of_shots = []
list_of_shots2 = []
list_of_shots3 = []

for ix in range(0, 100):
    field = seacombat_logic.get_arranged_ships()
    # field = {1: [{(10, 9, 0)}, {(7, 10, 0)}, {(5, 6, 0)}, {(1, 7, 0)}], 2: [{(3, 8, 0), (3, 9, 0)}, {(5, 8, 0), (5, 9, 0)}, {(8, 8, 0), (8, 7, 0)}], 3: [{(6, 3, 0), (6, 2, 0), (6, 4, 0)}, {(9, 2, 0), (9, 3, 0), (9, 4, 0)}], 4: [{(3, 2, 0), (3, 3, 0), (3, 4, 0), (3, 5, 0)}], 'misses': {}}
    # field = {1: [{(10, 4, 0)}, {(10, 6, 0)}, {(10, 8, 0)}, {(5, 4, 0)}], 2: [{(6, 10, 0), (5, 10, 0)}, {(8, 10, 0), (9, 10, 0)}, {(10, 1, 0), (10, 2, 0)}], 3: [{(1, 8, 0), (1, 6, 0), (1, 7, 0)}, {(3, 10, 0), (1, 10, 0), (2, 10, 0)}], 4: [{(1, 1, 0), (1, 2, 0), (1, 3, 0), (1, 4, 0)}], 'misses': set()}
    # field = {1: [{(8, 10, 0)}, {(7, 1, 0)}, {(4, 1, 0)}, {(5, 6, 0)}], 2: [{(1, 10, 0), (2, 10, 0)}, {(10, 7, 0), (10, 6, 0)}, {(10, 9, 0), (10, 10, 0)}], 3: [{(1, 8, 0), (1, 6, 0), (1, 7, 0)}, {(10, 1, 0), (10, 3, 0), (10, 2, 0)}], 4: [{(1, 1, 0), (1, 2, 0), (1, 3, 0), (1, 4, 0)}], 'misses': set()}
    for iy in range(0, 10):
        list_of_shots.append(alg1(field))
        list_of_shots2.append(alg2(field))
        list_of_shots3.append(alg3(field))


df = pd.DataFrame(list_of_shots, columns=['shots'])
df.index += 1
df2 = pd.DataFrame(list_of_shots2, columns=['shots'])
df2.index += 1
df3 = pd.DataFrame(list_of_shots3, columns=['shots'])
df3.index += 1

plt.scatter(x=df.index.values, y=df, alpha=0.7)
plt.axhline(y=df['shots'].mean(), color='lightblue', linestyle='--')
plt.scatter(x=df2.index.values, y=df2, c='r', alpha=0.7)
plt.axhline(y=df2['shots'].mean(), color='red', linestyle='--')
plt.scatter(x=df3.index.values, y=df3, c='g', alpha=0.7)
plt.axhline(y=df3['shots'].mean(), color='green', linestyle='--')
plt.xlabel('iteration number')
plt.ylabel('shots')
plt.show()
