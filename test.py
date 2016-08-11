from redcode import BattleProgram
from mars import Mars

programA = BattleProgram("DWARF_A", 1, "battle-programs/dwarf.rc")
programB = BattleProgram("DWARF_B", 1, "battle-programs/dwarf.rc")

N = 20

mars = Mars(programA, programB, N, num_it=1)
mars.execute_core_war()
