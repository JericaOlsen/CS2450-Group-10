from io import StringIO
from computer import Memory, CPU


def test_id10_1(monkeypatch, capsys):
    memory = Memory()
    cpu = CPU(memory, print, input)

    for i, instruction in enumerate([1097, 1098, 1099, 1197, 4300]):
        memory.set(i, instruction)

    monkeypatch.setattr('sys.stdin', StringIO("4\n7\nhey\n21\n"))
    cpu.execute()

    assert capsys.readouterr().out == "Enter a value for memory[97]: "\
                                      "Enter a value for memory[98]: "\
                                      "Enter a value for memory[99]: "\
                                      "Invalid input. Please enter an integer.\n"\
                                      "Enter a value for memory[99]: "\
                                      "Value at memory[97]: 4\n"\
                                      "Program halted.\n"
