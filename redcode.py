INSTRUCTION_MNEMONICS = [
                        "DAT",
                        "MOV",
                        "ADD",
                        "SUB",
                        "JMP",
                        "JMZ",
                        "JMG",
                        "DJZ",
                        "CMP",
                        ]

SINGLE_ARG_INSTRUCTIONS = ["JMP", "DAT"]

ADDRESS_MODES = ["#", "", "@"]

def compile_redcode(lines):
    """
    Compile an array of string (each one a line of redcode) into a list of
    of decimal instructions
    """

    def next_bit(s):
        if not s:
            raise SyntaxError("Nothing more to parse")
        spl = s.split(" ", 1)
        bit = spl[0]
        if len(spl) == 2:
            rest = spl[1]
        else:
            rest = ""
        return bit, rest

    def parse_arg(a):

        # Address mode part
        if a[0].isdigit() or (a[0] == "-"):
            mode_str = ""
            b = a
        else:
            mode_str = a[0]
            b = a[1:]
        if mode_str not in ADDRESS_MODES:
            raise SyntaxError("Unrecognised address mode: " + mode_str)
        mode = ADDRESS_MODES.index(mode_str)

        # Address part
        try:
            address = int(b)
        except:
            raise SyntaxError("Non-numerical address: " + b)

        return mode, address


    instructions = []

    for s in lines:
        s = s.strip()

        if s.startswith("//"):
            # Comment, ignore this line
            continue

        mnemonic, s = next_bit(s)
        if mnemonic not in INSTRUCTION_MNEMONICS:
            raise SyntaxError("Unrecognised instruction: " + mnemonic)
        code = INSTRUCTION_MNEMONICS.index(mnemonic)

        argA, s = next_bit(s)
        modeA, addressA = parse_arg(argA)

        if mnemonic not in SINGLE_ARG_INSTRUCTIONS:
            argB, s = next_bit(s)
            modeB, addressB = parse_arg(argB)
        else:
            modeB = 0
            addressB = 0

        if mnemonic == "DAT":
            addressB = addressA
            modeB = 0
            modeA = 0
            addressA = 0

        inst = Instruction(code, modeA, modeB, addressA, addressB)
        instructions.append(inst)

    return instructions

class Instruction:
    """
    A redcode instruction
    """
    def __init__(self, code, modeA, modeB, addressA, addressB):
        self.code = code
        self.modeA = modeA
        self.modeB = modeB
        self.addressA = addressA
        self.addressB = addressB


class BattleProgram:
    """
    Redcode battle program
    """

    def __init__(self, name, file):
        self.name = name

        with open(file, 'r') as f:
            lines = f.readlines()
        self.instructions = compile_redcode(lines)