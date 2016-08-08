from redcode import BattleProgram
from mars import Mars

programA = BattleProgram("DWARF_A", "battle-programs/dwarf.rc")
programB = BattleProgram("DWARF_B", "battle-programs/dwarf.rc")

N = 20

mars = Mars(programA, programB, N)
mars.execute_core_war()
