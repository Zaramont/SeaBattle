import json

import seacombat_logic


def convert_field_to_object_for_json(field):
    new_field = dict()
    new_field['misses'] = list()

    for key in range(1, 5):
        new_field[key] = list()
        ships = new_field[key]

        for ship in field[key]:
            new_ship = dict()
            new_ship['ship'] = list()
            for deck in ship:
                new_deck = dict()
                new_deck['row'] = deck[0]
                new_deck['column'] = deck[1]
                new_deck['state'] = deck[2]
                new_ship['ship'].append(new_deck)
            ships.append(new_ship)
    for miss in field['misses']:
        new_miss = dict()
        new_miss['row'] = miss[0]
        new_miss['column'] = miss[1]
        new_field['misses'].append(new_miss)
    return new_field


def convert_json_to_field(object):
    pass


field = seacombat_logic.get_arranged_ships()
field2 = seacombat_logic.get_arranged_ships()

def save_to_file(path, field, field2):
    obj = dict()
    obj['player_field'] = convert_field_to_object_for_json(field)
    obj['ai_field'] = convert_field_to_object_for_json(field2)

    encoded_struct = json.dumps(obj)
    f = open(path, 'w+')
    f.writelines(encoded_struct)
    f.close()

save_to_file('./resources/save_test.json', field,field2)
