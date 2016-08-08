import numpy as np
import time

from redcode import encode_instruction

class Mars:
    """
    Main class for executing and coordinating the core war
    """

    def __init__(self, programA, programB, N, num_it = 10):
        self.num_it = num_it
        self.N = N
        self.core = Core(N)
        startA = 0
        startB = int(N/2)
        self.playerA = Executor(programA, startA, self.core)
        self.playerB = Executor(programB, startB, self.core)

        self.core.display()

    def execute_core_war(self):

        for it in range(self.num_it):
            print("\nAfter {} cycles:".format(it))
            self.core.display()

            self.playerA.execute_instruction()
            self.playerB.execute_instruction()

            time.sleep(1)

        print("Nobody won. How dull.")

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

    # Add method to write constant, absolute and relative,
    #  and to read absolute and relative

    # Add method to draw a representation of the core

    def display(self):
        print("CORE:")
        for m in self.memory:
            format_str = "{:0" + str(3+2*self.M) + "}"
            print(format_str.format(m))

class Executor:
    """
    A competing process in the core war
    """

    def __init__(self, program, start, core):
        self.address = start
        self.core = core
        self.program = program

        # Write my instructions into the core
        add = self.address
        for inst in self.program.instructions:
            self.core.write_instruction(add, inst)
            add = core.next_address(add)



    def execute_instruction(self):

        # Read instruction

        # Execute it

        pass

