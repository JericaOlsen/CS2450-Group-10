import re
import sys

class Memory:
    """
    Simulates memory with exactly 250 integer storage locations,
    each capable of holding a signed six‑digit word.
    """
    MAX_LINES = 250
    MAX_WORD  =  999_999

    def __init__(self):
        self.length = Memory.MAX_LINES
        self.words = [0] * self.length

    def get(self, index: int) -> int:
        if 0 <= index < self.length:
            return self.words[index]
        raise IndexError(f"Memory index {index:03d} out of range")

    def set(self, index: int, value: int):
        if not (0 <= index < self.length):
            raise IndexError(f"Memory index {index:03d} out of range")
        if abs(value) > Memory.MAX_WORD:
            raise ValueError(f"Word overflow: |{value}| > {Memory.MAX_WORD}")
        self.words[index] = value


class CPU:
    """
    Basic CPU simulator:
     - Six‑digit words: ±000000…±999999
     - Three‑digit addresses: 000…249
     - Opcodes are still the same numeric codes (010→READ, 011→WRITE, … 043→HALT)
    """
    def __init__(self, memory: Memory, input_fn=input, output_fn=print):
        self.memory      = memory
        self.accumulator = 0
        self.cr          = 0  # instruction pointer
        self.input  = input_fn
        self.output = output_fn

    def check_overflow(self):
        if abs(self.accumulator) > Memory.MAX_WORD:
            self.output("Error: Overflow. Accumulator out of range.")
            sys.exit(1)

    def execute(self):
        while True:
            try:
                instr = self.memory.get(self.cr)
            except IndexError:
                self.output(f"Error: Instruction pointer {self.cr:03d} out of range.")
                break

            opcode, operand = divmod(instr, 1000)

            # validate operand address
            if not (0 <= operand < self.memory.length):
                self.output(f"Invalid memory address: {operand:03d}. Must be 000–249. Halting.")
                break

            match opcode:
                case 10:  self.read(operand)      # 010
                case 11:  self.write(operand)     # 011
                case 20:  self.load(operand)      # 020
                case 21:  self.store(operand)     # 021
                case 30:  self.add(operand)       # 030
                case 31:  self.subtract(operand)  # 031
                case 32:  self.divide(operand)    # 032
                case 33:  self.multiply(operand)  # 033
                case 40:  self.branch(operand)    # 040
                case 41:  self.branchneg(operand) # 041
                case 42:  self.branchzero(operand)# 042
                case 43:  # HALT (043)
                    self.output("Program halted.")
                    break
                case _:
                    self.output(f"Unknown opcode: {opcode:03d}. Halting.")
                    break

            self.cr += 1

    def read(self, addr):
        while True:
            try:
                val = int(self.input(f"Enter value for [{addr:03d}]: "))
                if abs(val) > Memory.MAX_WORD:
                    self.output(f"Error: |{val}| exceeds six‑digit limit.")
                    continue
                self.memory.set(addr, val)
                break
            except ValueError:
                self.output("Invalid input. Please enter an integer.")

    def write(self, addr):
        self.output(f"Value at [{addr:03d}]: {self.memory.get(addr)}")

    def load(self, addr):
        self.accumulator = self.memory.get(addr)
        self.check_overflow()

    def store(self, addr):
        self.memory.set(addr, self.accumulator)

    def add(self, addr):
        self.accumulator += self.memory.get(addr)
        self.check_overflow()

    def subtract(self, addr):
        self.accumulator -= self.memory.get(addr)
        self.check_overflow()

    def divide(self, addr):
        divisor = self.memory.get(addr)
        if divisor == 0:
            self.output("Error: Division by zero. Halting.")
            sys.exit(1)
        self.accumulator //= divisor
        self.check_overflow()

    def multiply(self, addr):
        self.accumulator *= self.memory.get(addr)
        self.check_overflow()

    def branch(self, target):
        if not (0 <= target < self.memory.length):
            self.output(f"Error: Branch target {target:03d} invalid. Halting.")
            sys.exit(1)
        self.cr = target - 1
        self.output(f"Branched to {target:03d}")

    def branchneg(self, target):
        if self.accumulator < 0:
            self.branch(target)
        else:
            self.output("Accumulator ≥ 0; no branch.")

    def branchzero(self, target):
        if self.accumulator == 0:
            self.branch(target)
        else:
            self.output("Accumulator ≠ 0; no branch.")


def load_program(filename: str, memory: Memory):
    """
    Reads up to 250 lines of six‑digit words from `filename` into `memory`.
    Lines must match optional '-' plus exactly 6 digits.
    """
    pattern = re.compile(r'^-?\d{6}$')
    with open(filename, 'r') as f:
        lines = [ln.rstrip('\n') for ln in f]

    if len(lines) > memory.length:
        raise ValueError(f"Program has {len(lines)} lines; max is {memory.length}.")

    for i, line in enumerate(lines):
        if not pattern.match(line):
            raise ValueError(f"Invalid word on line {i+1}: '{line}'. Must be ±000000–±999999.")
        memory.set(i, int(line))

    # zero out the rest
    for j in range(len(lines), memory.length):
        memory.set(j, 0)


def save_program(filename: str, memory: Memory):
    """
    Dumps all 250 memory words to `filename`, one per line,
    formatted as signed six‑digit numbers (with leading zeros).
    """
    with open(filename, 'w') as f:
        for i in range(memory.length):
            w = memory.get(i)
            sign = '-' if w < 0 else ''
            f.write(f"{sign}{abs(w):06d}\n")
