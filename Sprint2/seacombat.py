import seacombat_controller
import seacombat_logic

# f1 = seacombat_logic.get_arranged_ships()
# f2 = seacombat_logic.get_arranged_ships()
# seacombat_draw.show_dict_field(f1)
# seacombat_draw.show_dict_field(f2)
# seacombat_draw.start(f1,f2)
seacombat_controller.start(seacombat_logic.get_blank_field(), seacombat_logic.get_arranged_ships())
