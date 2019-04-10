import seacombat_logic
import seacombat_draw
# seacombat_draw.start(seacombat_logic.get_blank_field(), seacombat_logic.get_arranged_ships())
# seacombat_draw.start(seacombat_logic.get_arranged_ships(), seacombat_logic.get_arranged_ships())
# print(seacombat_logic.get_arranged_ships())
# print(seacombat_logic.is_ships_placement_legal(seacombat_logic.get_arranged_ships()))
# print(seacombat_logic.is_ships_placement_legal(seacombat_logic.get_blank_field()))
# set1 = set()
# set2 = set()
# set1.add((2, 2, 0))
# set2.add((2, 3, 0))
# set3 = {(3, 2, 0), (1, 1, 0), (2, 1, 0), (3, 1, 0), (2, 2, 0), (1, 3, 0), (2, 3, 0), (3, 3, 0), (1, 2, 0)}
# set4 = {(3, 2, 0), (2, 4, 0), (1, 4, 0), (3, 4, 0), (2, 2, 0), (1, 3, 0), (2, 3, 0), (3, 3, 0), (1, 2, 0)}
# print(set3 & set4)
# print(seacombat_logic.are_ships_touched(set1, set2))
seacombat_draw.show_dict_field(seacombat_logic.get_arranged_ships())
