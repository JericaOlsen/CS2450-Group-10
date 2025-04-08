from io import StringIO
from computer import Memory, CPU

def test_id3_1():
    """
        Test input
    """
    memory = Memory()

    for i, instruction in enumerate([1007, 1008, 1009, 3007, 3108, 3009, 4300]):
         memory.set(i, instruction)

    inputs = iter(['28','5','4'])
    def mock_input(prompt):
        return next(inputs)
    
    output = []
    def mock_output(message):
        output.append(message)

    cpu = CPU(memory, mock_output,mock_input)
    cpu.execute()
    assert memory.get(7) == 28
    assert memory.get(8) == 5
    assert memory.get(9) == 4
