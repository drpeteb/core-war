import numpy as np
import time

from redcode import encode_instruction, decode_instruction

class Mars:
    """
    Main class for executing and coordinating the core war
    """

    def __init__(self, program1, program2, N, num_it = 10):

        # Decide where to start the two players
        start1 = 0
        start2 = int(N/2)

        # Store constants
        self.num_it = num_it

        # Initialise core
        self.core = Core(N)

        # Initialise players
        self.name1 = program1
        self.address1 = start1 + program1.offset
        self.core.write_program(start1, program1.instructions)

        self.name2 = program2
        self.address2 = start2 + program2.offset
        self.core.write_program(start2, program2.instructions)

        # Diplay the starting state of the memory
        print("CORE[t=0]:")
        self.core.display()

    def execute_core_war(self):

        for it in range(self.num_it):

            lost = self.core.execute_instruction(self.address1)
            if lost:
                print("{} wins".format(self.player2.name))
            self.address1 = self.core.next_address(self.address1)

            lost = self.core.execute_instruction(self.address2)
            if lost:
                print("{} wins".format(self.player1.name))
            self.address2 = self.core.next_address(self.address2)

            time.sleep(1)

            print("\nCORE[t={}]:".format(it + 1))
            self.core.display()

        print("\nNobody won. How dull.")



class Core:
    """
    'Core' memory, in which the war shall be fought
    """

    def __init__(self, N):
        self.N = N                          # Number of memory addresses
        self.M = int(np.log10(N)) + 1       # Number of digits for addresses
        self.memory = np.zeros(N, dtype=int)

    def next_address(self, add):
        return (add + 1) % self.N

    def write_instruction(self, address, inst):
        self.memory[address] = encode_instruction(inst, self.N, self.M)

    def write_program(self, start, instructions):
        add = start
        for inst in instructions:
            self.write_instruction(add, inst)
            add = self.next_address(add)

    def execute_instruction(self, address):
        mem = self.memory[address]
        inst = decode_instruction(mem, self.M)

        print("")
        print(inst)

        if inst.code == 0:
            """DAT"""
            return True
        elif inst.code == 1:
            """MOV"""

            return False
        elif inst.code == 2:
            """ADD"""

            return False
        elif inst.code == 3:
            """SUB"""

            return False
        elif inst.code == 4:
            """JMP"""

            return False
        elif inst.code == 5:
            """JMZ"""

            return False
        elif inst.code == 6:
            """JMG"""

            return False
        elif inst.code == 7:
            """DJZ"""

            return False
        elif inst.code == 8:
            """CMP"""

            return False
        else:
            raise RuntimeError("Invalid redcode instruction code: " + inst.code)

    def display(self):
        for m in self.memory:
            format_str = "{:0" + str(3+2*self.M) + "}"
            print(format_str.format(m))


