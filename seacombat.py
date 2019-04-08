import seacombat_draw
import seacombat_logic

# seacombat_draw.show_battlefield(seacombat_logic.field)
# seacombat_draw.show_array(seacombat_logic.field)
# seacombat_draw.start(seacombat_logic.get_blank_field(), seacombat_logic.get_arranged_ships())
# seacombat_draw.start(seacombat_logic.get_arranged_ships(), seacombat_logic.get_arranged_ships())

print(seacombat_logic.is_ships_placement_legal(seacombat_logic.get_arranged_ships()))