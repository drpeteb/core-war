from redcode import BattleProgram
from mars import Mars

programA = BattleProgram("DWARF", 1, "battle-programs/dwarf.rc")
programB = BattleProgram("IMP", 0, "battle-programs/imp.rc")

N = 20

mars = Mars(programA, programB, N, num_it=20)
mars.execute_core_war()
