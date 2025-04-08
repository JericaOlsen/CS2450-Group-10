from io import StringIO
from computer import Memory, CPU


def test_id6_1():
    """
        Test input
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

    assert memory.get(50) == 5
    assert memory.get(51) == 5
