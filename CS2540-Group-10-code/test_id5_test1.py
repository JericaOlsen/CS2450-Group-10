from unittest.mock import patch
from computer import CPU, Memory

def test_cpu_branching():
    memory = Memory()

    program = [1088, 1089, 1050, 3088, 3189, 4150, 4300]
    for i, instruction in enumerate(program):
        memory.set(i, instruction)
    
    inputs = iter(['3','9','22'])
    def mock_input(prompt):
        return next(inputs)
    
    output = []
    def mock_output(message):
        output.append(message)

    cpu = CPU(memory, mock_output,mock_input)
    cpu.execute()
    
    assert memory.get(88) == 3 
    assert memory.get(89) == 9
    
    assert cpu.accumulator == -6
    
    print(f'Control Register after branching: {cpu.cr}')
    assert cpu.cr == 50

