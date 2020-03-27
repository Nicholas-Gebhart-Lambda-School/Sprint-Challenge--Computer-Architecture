"""
Implementation of the LS-8 emulator

The LS-8 is an 8-bit computer with 8-bit memory addressing.

An 8-bit CPU contains 256 bytes of memory and can compute values
up to 255. Theoretically, we cna support up to 256 instructions.
"""

import sys                          # Receives file name from sys argv


# ===============================================================
# Constants =====================================================
# ===============================================================

E = -1                              # Equality flag
G = None                            # Greater than flag
L = None                            # Less than flag

# ===============================================================
# Errors ========================================================
# ===============================================================

EXIT_FAILURE = "\nERROR: PROCESS RETURNED NON-ZERO EXIT CODE"
EXIT_SUCCESS = "SUCCESS\n"
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


# Stretch
AND = 0b10100001                    # Binary bitwise AND operator
BOR = 0b10100101                    # Binary bitwise OR operatior
NOT = 0b01101110                    # Unary bitwise NOT operator
SHL = 0b10101011                    # Binary bitshift left operator
SHR = 0b10101100                    # Binary bitshift right operator
MOD = 0b10100110                    # Binary modulus operator
XOR = 0b10101001                    # Binary bitwise XOR operator


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
            PRN: self._dispatch_prn,
            JMP: self._dispatch_jmp,
            CMP: self._dispatch_cmp,
            JEQ: self._dispatch_jeq,
            JNE: self._dispatch_jne,
            LDI: self._dispatch_ldi,
            HLT: self._dispatch_hlt,
            # Stretch
            AND: self._dispatch_and,
            BOR: self._dispatch_bor,
            NOT: self._dispatch_not,
            SHL: self._dispatch_shl,
            SHR: self._dispatch_shr,
            MOD: self._dispatch_mod,
            XOR: self._dispatch_xor
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

        if operation == 'CMP':
            if self.register[register_a] \
                    == self.register[register_b]:
                self.flags[E] = 1
            else:
                self.flags[E] = 0

    # ===============================================================
    # Dispatch table ================================================
    # ===============================================================

    def _dispatch_prn(self):
        """
        Pseudo-instruction to print current MDR
        """

        print(self.register[self.ram_read(self.counter + 1)])
        self.counter += 2

    def _dispatch_jmp(self):
        """
        Jumps to the address stored at a given register.
        Sets the program counter to the address stored in a given register.
        """

        next_register = self.ram_read(self.counter + 1)
        self.counter = self.register[next_register]

    def _dispatch_jeq(self):
        """
        If the E flag is truthy, jump to the given register,
        otherwise continue program execution at the next MAR
        """

        if self.flags[E] == 1:
            next_register = self.ram_read(self.counter + 1)
            self.counter = self.register[next_register]
        else:
            self.counter += 2

    def _dispatch_jne(self):
        """
        If the E flag is falsy, jump to the given register,
        otherwise continue progrm execution at the next MAR
        """

        if self.flags[E] == 0:
            next_register = self.ram_read(self.counter + 1)
            self.counter = self.register[next_register]
        else:
            self.counter += 2

    def _dispatch_ldi(self):
        """
        Sets the value of a register to an integer
        """

        self.register[self.ram_read(self.counter + 1)]\
            = self.ram_read(self.counter + 2)
        self.counter += 3

    def _dispatch_hlt(self):
        """
        Halt the CPU execution and exit with status code 0
        """

        self.counter = 0
        print(EXIT_SUCCESS)
        sys.exit(0)

    def _dispatch_cmp(self):
        """
        Compares the values at to registers:

        If registerA is less than registerB, set L to 1, otherwise 0
        If registerA is greater than registerB, set G to 1, otherwise 0
        If registerA is equal to registerB, set E to 1, otherwise 0
        """
        register_a = self.ram_read(self.counter + 1)
        register_b = self.ram_read(self.counter + 2)

        self._alu('CMP', register_a, register_b)
        self.counter += 3

    # ===============================================================
    # Stretch methods ===============================================
    # ===============================================================

    def _dispatch_and(self):
        """
        Performs a logical AND operation on each MDR

        1 x 1 = 1
        1 x 0 = 0
        0 x 0 = 0
        """

    def _dispatch_bor(self):
        """
        Performs a logical inclusive OR operation on each MDR

        00000101 | 00000011 = 00000111
        """

    def _dispatch_not(self):
        """
        Performs a logical negation on each bit for one MDR

        ~ 00000111 = 00001000
        """

    def _dispatch_shl(self):
        """
        Performs an arithmetic left shift
        Zeros are shifted in on the right

        00010111 = 00101110
        """

    def _dispatch_shr(self):
        """
        Performs an arithmetic right shift
        The sign bit is shifted onto the left

        10010111 = 11001011
        """

    def _dispatch_mod(self):
        """
        Performs a module operation between two MDR inputs
        Result is the remainder after division

        00011010 % 11001010 = 0011010
        """

    def _dispatch_xor(self):
        """
        Takes two bit patterns of equal length and performs the
        logical exclusive OR operation on each corresponding bit

        00000101 ^ 00000011 = 00000110
        """


if __name__ == "__main__":
    if len(sys.argv) == 2:
        FILE = sys.argv[1]          # Receive file from arguments
        CPU = CPU()                 # Instantiate the LS-8
        CPU.run(FILE)               # Invoke main with given file
    else:
        print(EXIT_FAILURE, USAGE)  # Prints usage error message
        sys.exit(1)                 # Non-zero exit code
