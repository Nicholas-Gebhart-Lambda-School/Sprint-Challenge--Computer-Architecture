"""
Implementation of the LS-8 emulator

The LS-8 is an 8-bit computer with 8-bit memory addressing.

An 8-bit CPU contains 256 bytes of memory and can compute values
up to 255. Theoretically, we cna support up to 256 instructions.
"""

import sys                          # Receives file name from sys argv

# ===============================================================
# Instructions ==================================================
# ===============================================================

"""
Bits in the byte: AABCDDDD

AA  : Number of operands for the operation, 0 - 2
B   : 1 if this is an ALU operation
C   : 1 if this instruction sets the Program Counter
DDDD: Instruction identifier
"""

CMP = 0b10100111                    # Comparison instruction, sets LGE flags
LDI = 0b10000010                    # Sets the value of a register
PRN = 0b01000111                    # Pseudo-instruction, prints subsequent MDR
JMP = 0b01010100                    # Jump instruction, moves pointer to MAR
JEQ = 0b01010101                    # Jumps to MAR if E flag is truthy
JNE = 0b01010110                    # Jumps to MAR if E flag is falsy
HLT = 0b00000001                    # Halt program execution


# ===============================================================
# CPU Class =====================================================
# ===============================================================


class CPU:
    """
    Initialize a CPU class which matches the LS-8 spec.
    """

    def __init__(self):
        """
        Register: an 8-bit register holding values between 0 - 255.
        RAM: 256 bytes of memory to store our program.
        Flags: An 8-bit register holding the flag status: 00000LGE.
        Counter: Program counter, address of the current instruction.
        Dispatch: A branch table to efficiently execute instructions.
        """

        self.register = [0] * 8     # 8-bit instruction register
        self.ram = [0] * 256        # 256 bytes of memory
        self.flags = [0] * 8        # 8-bit flag register
        self.counter = 0            # Program counter
        self.dispatch = {           # Branch table
            'value': 'method',
            'value1': 'method1',
            'value2': 'method2',
        }

    # ===============================================================
    # Public methods ================================================
    # ===============================================================

    def ram_write(self, mar, mdr):
        """
        MDR: Memory Data Register, holds the value in a register
        MAR: Memory Address Register, holds the memory address location

        Procedure to write the MDR at the given MAR
        """
        self.ram[mar] = mdr

    def ram_read(self, mar):
        """
        MAR: Memory Address Register, holds the memory address location

        Function to read the value at the MAR
        """
        return self.ram[mar]

    def load(self, file):
        """
        Procedure to load a program into memory.

        Splits lines at the '#' delimiter and strips whitespace
        to pass instructions to ram_write.

        Raises an exception if sys.argv[1] is invalid.
        """

    def run(self, file):
        """
        Acts as main for the CPU class
        Receives a program from sys.argv[1] and passes it to self.load

        Initializes a REPL and dispatches actions from the branchtable
        """


if __name__ == "__main__":
    if len(sys.argv) == 2:
        pass
