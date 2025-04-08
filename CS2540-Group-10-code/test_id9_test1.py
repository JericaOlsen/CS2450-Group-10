from computer import Memory, CPU

def test_id9_1(capsys):
    memory = Memory()
    cpu = CPU(memory, print, input)

    for i, instruction in enumerate([1100, 1101, 1102, 4300]):
        memory.set(i, instruction)
    inputs = []
    def mock_input(prompt):
        return next(inputs)
    
    output = []
    def mock_output(message):
        output.append(message)

    cpu = CPU(memory, mock_output,mock_input)
    cpu.execute()
    output = ''.join(output)
    expected_output = "Value at memory[0]: 1100Value at memory[1]: 1101Value at memory[2]: 1102Program halted."
    assert expected_output == output