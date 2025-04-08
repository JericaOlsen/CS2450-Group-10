from io import StringIO
from computer import Memory, CPU

def test_id6_2():
    """
        Test result
    """
    memory = Memory()

    for i, instruction in enumerate([1050, 1051, 2050, 3151, 4206, 1152, 4300]):
        memory.set(i, instruction)

    inputs = iter(['5','5'])
    def mock_input(prompt):
        return next(inputs)
    
    output = []
    def mock_output(message):
        output.append(message)

    cpu = CPU(memory, mock_output,mock_input)
    cpu.execute()

    assert cpu.accumulator == 0
    assert cpu.cr == 6
