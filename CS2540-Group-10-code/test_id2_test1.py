import pytest
from computer import CPU, Memory  


def load_instructions_and_data(memory, instructions, data_start, data_values):
    for i, instr in enumerate(instructions):
        memory.set(i, instr)

    for i, value in enumerate(data_values):
        memory.set(data_start + i, value)

def test_store_binary_message():
    memory = Memory()
    instructions = [1020,1021,1022,1023,1024,1025,1026,1027, 
                    1120,1121,1122,1123,1124,1125,1126,1127, 4300]

    binary_message = [1, 0, 2, 0, 1, 6, 10, 1]

    load_instructions_and_data(memory, instructions, 20, binary_message)

    for i, value in enumerate(binary_message):
        assert memory.get(20 + i) == value, f"Memory at {20 + i} should be {value}"

def test_write_binary_message():
    memory = Memory()
    instructions = [1020,1021,1022,1023,1024,1025,1026,1027, 
                    1120,1121,1122,1123,1124,1125,1126,1127, 4300]

    binary_message = [1, 0, 2, 0, 1, 6, 10, 1]

    load_instructions_and_data(memory, instructions, 20, binary_message)
    inputs = iter(['1','0','2','0','1','6','10','1'])
    def mock_input(prompt):
        return next(inputs)
    
    output = []
    def mock_output(message):
        output.append(message)

    cpu = CPU(memory, mock_output,mock_input)

    cpu.execute()

    expected_output = [f"Value at memory[{20 + i}]: {binary_message[i]}" for i in range(len(binary_message))]
    expected_output.append('Program halted.')
    output = ' '.join(output)
    expected_output = ' '.join(expected_output)
    assert output == expected_output, f"\nExpected:\n{expected_output}\nGot:\n{output}"
