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


if __name__ == "__main__":
    if len(sys.argv) == 2:
        pass
