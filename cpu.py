"""
Implementation of the LS-8 emulator

The LS-8 is an 8-bit computer with 8-bit memory addressing.

An 8-bit CPU contains 256 bytes of memory and can compute values
up to 255. Theoretically, we cna support up to 256 instructions.
"""

import sys                          # Receives file name from sys argv


# ===============================================================
# Errors ========================================================
# ===============================================================

EXIT_FAILURE = "\nERROR: PROCESS RETURNED NON-ZERO EXIT CODE"
FILE_NAME = f"\nUNKNOWN FILE: cannot find file with name {sys.argv[1]}"
NOT_FOUND = f"\nOPERATION UNKNOWN: Opcode not found, "
USAGE = f"\nUSAGE: python {sys.argv[0]} [file-name].ls8"

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

        try:
            address = 0
            with open(file) as program:
                for line in program:
                    value = line.split('#')[0].strip()

                    if value != '':
                        instruction = int(value, 2)
                        self.ram_write(address, instruction)
                        address += 1
                    else:
                        continue
        except FileNotFoundError:
            print(EXIT_FAILURE, FILE_NAME)
            sys.exit(2)

    def run(self, file):
        """
        Acts as main for the CPU class
        Receives a program from sys.argv[1] and passes it to self.load

        Initializes a REPL and dispatches actions from the branchtable
        """

        self.load(file)

        while True:
            operation = self.ram_read(self.counter)

            if operation in self.dispatch:
                self.dispatch[operation]()
            else:
                raise Exception(NOT_FOUND, operation)

    # ===============================================================
    # Private methods ===============================================
    # ===============================================================

    def _alu(self, operation, register_a, register_b):
        """
        Arithmetic Logic Unit

        Procedures that handle arithmetic operations,
        bitwise logical operations, and bitshift operations.
        """

    # ===============================================================
    # Dispatch table ================================================
    # ===============================================================

    def _dispatch_prn(self):
        """
        Pseudo-instruction to print current MDR
        """

    def _dispatch_jmp(self):
        """
        Jumps to the address stored at a given register.
        Sets the program counter to the address stored in a given register.
        """

    def _dispatch_jeq(self):
        """
        If the E flag is truthy, jump to the given register,
        otherwise continue program execution at the next MAR
        """

    def _dispatch_jne(self):
        """
        If the E flag is falsy, jump to the given register,
        otherwise continue progrm execution at the next MAR
        """

    def _dispatch_ldi(self):
        """
        Sets the value of a register to an integer
        """

    def _dispatch_hlt(self):
        """
        Halt the CPU execution and exit with status code 0
        """

    def _dispatch_cmp(self):
        """
        Compares the values at to registers:

        If registerA is less than registerB, set L to 1, otherwise 0
        If registerA is greater than registerB, set G to 1, otherwise 0
        If registerA is equal to registerB, set E to 1, otherwise 0
        """


if __name__ == "__main__":
    if len(sys.argv) == 2:
        FILE = sys.argv[1]          # Receive file from arguments
        CPU = CPU()                 # Instantiate the LS-8
        CPU.run(FILE)               # Invoke main with given file
    else:
        print(EXIT_FAILURE, USAGE)  # Prints usage error message
        sys.exit(1)                 # Non-zero exit code
