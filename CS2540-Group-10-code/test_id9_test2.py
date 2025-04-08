from computer import Memory, CPU

def test_id9_2():
    memory = Memory()
    cpu = CPU(memory, print, input)

    for i, instruction in enumerate([1100, 1101, 1102, 4300]):
        memory.set(i, instruction)

    cpu.execute()

    assert memory.get(3) == 4300

