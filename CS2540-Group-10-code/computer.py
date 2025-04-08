class CPU:
    """
    Simulates a basic CPU that executes simple machine instructions stored in memory.
    The CPU has an accumulator for arithmetic operations and a control register (cr) for instruction tracking.
    Now supports six-digit words and three-digit memory addresses (000 to 249).
    """

    def __init__(self, memory, output, input):
        self.memory: Memory = memory
        self.accumulator: int = 0  # Accumulator
        self.cr: int = 0  # Control register
        self.output = output
        self.input = input

    def check_overflow(self):
        if abs(self.accumulator) > 999999:
            self.output("Error: Overflow. Accumulator out of range.")
            exit(1)

    def execute(self):
        """
        Executes instructions stored in memory until a HALT instruction (opcode 043) is encountered.
        """
        while True:
            try:
                instruction = self.memory.get(self.cr)
            except IndexError:
                self.output("Error: Instruction pointer out of range. Halting execution.")
                break
            # Split the six-digit instruction into opcode and operand (operand is in the last 3 digits)
            opcode, operand = divmod(instruction, 1000)
            if not (0 <= operand < self.memory.length):
                self.output(f"Invalid memory address: {operand}. Must be between 000 and 249. Halting execution.")
                break

            match opcode:
                # I/O operations
                case 10:  # READ (010)
                    self.read(operand)
                case 11:  # WRITE (011)
                    self.write(operand)
                # Load/store operations
                case 20:  # LOAD (020)
                    self.load(operand)
                case 21:  # STORE (021)
                    self.store(operand)
                # Arithmetic operations
                case 30:  # ADD (030)
                    self.add(operand)
                case 31:  # SUBTRACT (031)
                    self.subtract(operand)
                case 32:  # DIVIDE (032)
                    self.divide(operand)
                case 33:  # MULTIPLY (033)
                    self.multiply(operand)
                # Control operations
                case 40:  # BRANCH (040)
                    self.branch(operand)
                case 41:  # BRANCHNEG (041)
                    self.branchneg(operand)
                case 42:  # BRANCHZERO (042)
                    self.branchzero(operand)
                case 43:  # HALT (043)
                    self.output("Program halted.")
                    break
                case _:
                    self.output(f"Unknown opcode: {opcode}. Halting execution.")
                    break
            self.cr += 1

    def read(self, operand):
        while True:
            try:
                value = int(self.input(f"Enter a value for memory[{operand:03d}]: "))
                # Ensure the input value is within six-digit limits
                if abs(value) > 999999:
                    self.output("Error: Input value exceeds six-digit limits.")
                    continue
                self.memory.set(operand, value)
                break
            except ValueError:
                self.output("Invalid input. Please enter an integer.")

    def write(self, operand):
        value = self.memory.get(operand)
        self.output(f"Value at memory[{operand:03d}]: {value}")

    def load(self, operand):
        self.accumulator = self.memory.get(operand)
        self.check_overflow()

    def store(self, operand):
        self.memory.set(operand, self.accumulator)

    def add(self, operand):
        self.accumulator += self.memory.get(operand)
        self.check_overflow()

    def subtract(self, operand):
        self.accumulator -= self.memory.get(operand)
        self.check_overflow()

    def divide(self, operand):
        divisor = self.memory.get(operand)
        if divisor == 0:
            self.output("Error: Division by zero. Halting execution.")
            exit(1)
        self.accumulator //= divisor
        self.check_overflow()

    def multiply(self, operand):
        self.accumulator *= self.memory.get(operand)
        self.check_overflow()

    def branch(self, index):
        if not (0 <= index < self.memory.length):
            self.output(f"Error: Invalid branch target {index}. Must be between 000 and {self.memory.length - 1}.")
            exit(1)
        self.cr = index - 1
        self.output("You have branched to location " + f"{index:03d}")

    def branchneg(self, index):
        if self.accumulator < 0:
            self.branch(index)
        else:
            self.output("Accumulator isn't negative; no branching.")

    def branchzero(self, index):
        if self.accumulator == 0:
            self.branch(index)
        else:
            self.output("Accumulator isn't zero; no branching.")

class Memory:
    """
    Simulates memory with a fixed number of integer storage locations.
    """
    def __init__(self, length=250):
        self.length = length  # Memory size increased to 250
        self.words = [0] * length

    def get(self, index) -> int:
        if 0 <= index < self.length:
            return self.words[index]
        raise IndexError("Memory index out of range")

    def set(self, index: int, value: int):
        if 0 <= index < self.length:
            self.words[index] = value
        else:
            raise IndexError("Memory index out of range")
