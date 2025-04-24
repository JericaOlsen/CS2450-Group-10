from tkinter import messagebox


def convert_program_format(program_file_name):
    old_instructions = []
    new_instructions = []
    with open(program_file_name, "r") as program_file:
        for line in program_file:
            try:
                word = int(line)

                if -9999 > word or 9999 < word:
                    messagebox.showerror(f'"{line}" is not valid instruction')
                    return False

                old_instructions.append(word)
            except ValueError:
                messagebox.showerror(f'"{line}" is not valid instruction')
                return False

    for instruction in old_instructions:
        opcode, operand = divmod(abs(instruction), 100)  # Extract opcode and operand

        new_instructions.append(
            (1 if instruction > 0 else -1) * (((opcode) * 1000) + operand)
        )  # Recombine opcode and operand in the new format

    with open(program_file_name, "w") as program_file:
        for word in new_instructions:
            program_file.write(f"{'-' if word < 0 else ''}{abs(word):06d}\n")

    return True


def main(args):
    if len(args) < 2:
        print("Too few arguments.")
        return 1
    elif len(args) > 2:
        print("Too many arguments.")
        return 1
    convert_program_format(args[1])
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main(sys.argv))
