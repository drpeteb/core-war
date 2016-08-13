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
        start2 = int(N / 2 + 1)

        # Store constants
        self.num_it = num_it

        # Initialise core
        self.core = Core(N)

        # Initialise players
        self.name1 = program1.name
        self.pointer1 = start1 + program1.offset
        self.core.write_program(start1, program1.instructions)

        self.name2 = program2.name
        self.pointer2 = start2 + program2.offset
        self.core.write_program(start2, program2.instructions)

        # Diplay the starting state of the memory
        print("CORE[t=0]:")
        self.core.display(self.pointer1, self.pointer2)

    def execute_core_war(self):

        for it in range(self.num_it):

            print("{} to move:".format(self.name1))
            self.pointer1 = self.core.execute_instruction(self.pointer1)
            if self.pointer1 is None:
                print("\n{} wins".format(self.name2))
                return

            print("{} to move:".format(self.name2))
            self.pointer2 = self.core.execute_instruction(self.pointer2)
            if self.pointer2 is None:
                print("\n{} wins".format(self.name1))
                return

            time.sleep(1)

            print("\nCORE[t={}]:".format(it + 1))
            self.core.display(self.pointer1, self.pointer2)

        print("\nNobody won. How dull.")



class Core:
    """
    'Core' memory, in which the war shall be fought, and associated logic
    for executing instructions.
    """

    def __init__(self, N):
        self.N = N                          # Number of memory addresses
        self.M = int(np.log10(N)) + 1       # Number of digits for addresses
        self.memory = (10**(self.M*2+3)-1) * np.ones(N, dtype=int)

    def next_address(self, add):
        return (add + 1) % self.N

    def write_instruction(self, address, inst):
        self.memory[address] = encode_instruction(inst, self.N, self.M)

    def write_program(self, start, instructions):
        add = start
        for inst in instructions:
            self.write_instruction(add, inst)
            add = self.next_address(add)

    def dereference_address(self, mode, argument, pointer):
        if mode == 0:
            return None
        elif mode == 1:
            return (pointer + argument) % self.N
        elif mode == 2:
            intermediate = (pointer + argument) % self.N
            return (intermediate + self.memory[intermediate]) % self.N

    def execute_instruction(self, pointer):
        mem = self.memory[pointer]
        inst = decode_instruction(mem, self.M)

        print("")
        print(inst)

        addressA = self.dereference_address(inst.modeA, inst.argumentA, pointer)
        addressB = self.dereference_address(inst.modeB, inst.argumentB, pointer)

        if addressA is None:
            dataA = inst.argumentA
        else:
            dataA = self.memory[addressA]

        if addressB is None:
            dataB = inst.argumentA
        else:
            dataB = self.memory[addressA]

        if inst.code == 0:
            """DAT"""
            return None

        elif inst.code == 1:
            """MOV"""
            if addressB is None:
                raise RuntimeError("Second argument cannot use direct addressing:\n{}".format(str(inst)))
            self.memory[addressB] = dataA
            return self.next_address(pointer)

        elif inst.code == 2:
            if addressB is None:
                raise RuntimeError("Second argument cannot use direct addressing:\n{}".format(str(inst)))
            """ADD"""
            self.memory[addressB] += dataA
            return self.next_address(pointer)

        elif inst.code == 3:
            """SUB"""
            if addressB is None:
                raise RuntimeError("Second argument cannot use direct addressing:\n{}".format(str(inst)))
            self.memory[addressB] -= dataA
            return self.next_address(pointer)

        elif inst.code == 4:
            """JMP"""
            if addressA is None:
                raise RuntimeError("Cannot use direct addressing for a jump:\n{}".format(str(inst)))
            return addressA

        elif inst.code == 5:
            """JMZ"""
            if addressA is None:
                raise RuntimeError("Cannot use direct addressing for a jump:\n{}".format(str(inst)))
            if dataB == 0:
                return addressA
            else:
                return self.next_address(pointer)

        elif inst.code == 6:
            """JMG"""
            if addressA is None:
                raise RuntimeError("Cannot use direct addressing for a jump:\n{}".format(str(inst)))
            if dataB > 0:
                return addressA
            else:
                return self.next_address(pointer)

        elif inst.code == 7:
            """DJZ"""
            if addressB is None:
                raise RuntimeError("Second argument cannot use direct addressing:\n{}".format(str(inst)))
            if addressA is None:
                raise RuntimeError("Cannot use direct addressing for a jump:\n{}".format(str(inst)))
            self.memory[addressB] -= 1
            if self.memory[addressB] == 0:
                return addressA
            else:
                return self.next_address(pointer)

        elif inst.code == 8:
            """CMP"""
            if dataA == dataB:
                return self.next_address(pointer)
            else:
                return self.next_address_n(self.next_address(pointer))

        else:
            raise RuntimeError("Invalid redcode instruction code: ".format(inst.code))

    def display(self, p1, p2):
        for idx, mem in enumerate(self.memory):
            format_str = "{:0" + str(3+2*self.M) + "}"
            if idx == p1:
                format_str += "*1"
            if idx == p2:
                format_str += "*2"
            print(format_str.format(mem))
