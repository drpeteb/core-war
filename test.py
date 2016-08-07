from redcode import BattleProgram
from mars import Mars

programA = BattleProgram("DWARF_A", "battle-programs/dwarf.rc")
programB = BattleProgram("DWARF_B", "battle-programs/dwarf.rc")

N = 8000

mars = Mars(programA, programB, N)

#        inst = "{:01}{:01}{:01}{:04}{:04}".format(code, modeA, modeB, addressA, addressB)
