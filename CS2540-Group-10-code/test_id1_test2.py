import computer
from io import StringIO

def test_student12():
    inst = [+1007, +1008, + 1009, +3007, +3108, +3009, +4300]

    memory = computer.Memory()

    for i, inst in enumerate(inst):
        memory.set(i, inst)

    inputs = iter(['10','7','2'])
    def mock_input(prompt):
        return next(inputs)
    
    output = []
    def mock_output(message):
        output.append(message)

    cpu = computer.CPU(memory, mock_output,mock_input)



    #User inputs 10 then 7 then 2
    cpu.execute()
    assert cpu.accumulator == 5
