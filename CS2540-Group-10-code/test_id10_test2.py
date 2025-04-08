from io import StringIO
from computer import Memory, CPU


def test_id10_2(monkeypatch):
    memory = Memory()
    cpu = CPU(memory, print, input)

    for i, instruction in enumerate([1097, 1098, 1099, 1197, 4300]):
        memory.set(i, instruction)

    monkeypatch.setattr('sys.stdin', StringIO("4\n7\nhey\n21\n"))
    cpu.execute()

    assert memory.get(97) == 4
    assert memory.get(98) == 7
    assert memory.get(99) == 21
