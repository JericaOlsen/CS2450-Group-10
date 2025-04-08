import computer
from io import StringIO

def test_student41(monkeypatch):
    inst = [+1021, +1033, +1027, +4006, +1028, +2027, +3321, +2122, +1122, +4300]

    memory = computer.Memory()

    for i, inst in enumerate(inst):
        memory.set(i, inst)

    inputs = iter(['0','4','7'])
    def mock_input(prompt):
        return next(inputs)
    
    output = []
    def mock_output(message):
        output.append(message)

    cpu = computer.CPU(memory, mock_output,mock_input)
    #User inputs 0 then 4 then 7
    cpu.execute()
    assert cpu.accumulator == 0
