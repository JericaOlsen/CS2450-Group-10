import pytest
from unittest.mock import patch
from computer import CPU, Memory


def test_branching_with_negative_accumulator():
    memory = Memory()
    instructions = [1088, 1089, 1050, 3088, 3189, 4150, 4300]
    for i, instruction in enumerate(instructions):
        memory.set(i, instruction)
    inputs = iter(['3','9','22'])
    def mock_input(prompt):
        return next(inputs)
    
    output = []
    def mock_output(message):
        output.append(message)

    cpu = CPU(memory, mock_output,mock_input)
    cpu.execute()
    assert cpu.accumulator == -6, "Accumulator should be -6 after operations"
    assert cpu.cr == 50, "CPU should have branched to location 50 due to negative accumulator"
