import computer
from io import StringIO

def test_teacher72(monkeypatch):
    inst = [+1060, +1061, +1062, +1063, +2060, +3361, +3362, +3363, +2164, +1164, +4300]

    memory = computer.Memory()

    for i, inst in enumerate(inst):
        memory.set(i, inst)

    inputs = iter(['24','24','24','24'])
    def mock_input(prompt):
        return next(inputs)
    
    output = []
    def mock_output(message):
        output.append(message)

    cpu = computer.CPU(memory, mock_output,mock_input)
    #User inputs 24 four times
    cpu.execute()
    assert cpu.accumulator == 331776 
