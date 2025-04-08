import pytest
from test_id2_test1 import load_instructions_and_data
from computer import CPU, Memory  


def test_store_and_write_new_binary_message():
    memory = Memory()

    instructions = [1030,1031,1032,1033,1034,1035,1036,1037, 
                    1130,1131,1132,1133,1134,1135,1136,1137, 4300]

    new_binary_message = [0, 1, 3, 2, 5, 7, 4, 2]

    load_instructions_and_data(memory, instructions, 30, new_binary_message)

    inputs = iter(['0','1','3','2','5','7','4','2'])
    def mock_input(prompt):
        return next(inputs)
    
    output = []
    def mock_output(message):
        output.append(message)

    cpu = CPU(memory, mock_output,mock_input)

    cpu.execute()

    expected_output = [f"Value at memory[{30 + i}]: {new_binary_message[i]}" for i in range(len(new_binary_message))]
    expected_output.append("Program halted.")
    expected_output = ' '.join(expected_output)

    output = ' '.join(output)
    assert output == expected_output, f"\nExpected:\n{expected_output}\nGot:\n{output}"

