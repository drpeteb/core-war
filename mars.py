import numpy as np

class Mars:
    """
    Main class for executing and coordinating the core war
    """

    def __init__(self, programA, programB, N, startA, startB):
        self.N = N
        self.core = Core()
        self.playerA = Executor(programA, startA, self.core)
        self.playerB = Executor(programB, startB, self.core)

    def execute_core_war(self):

        # Loop

            # Execute A instruction

            # Execute B instruction

        pass

class Core:
    """
    'Core' memory, in which the war shall be fought
    """

    def __init__(self, N):
        self.N = N
        self.memory = np.zero(N)

    # Add method to write constant, absolute and relative,
    #  and to read absolute and relative

    # Add method to draw a representation of the core

class Executor:
    """
    A competing process in the core war
    """

    def __init__(self, program, start, core):
        self.address = start
        self.core = core
        self.program = program

        # Write my instructions into the core

    def execute_instruction():

        # Read instruction

        # Execute it

        pass