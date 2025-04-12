from tkinter import messagebox

def convert_program_format(program_file_name):
  old_instructions = []
  new_instructions = []
  with open(program_file_name, "r") as program_file:
    for line in program_file:
      try:
        word = int(line)

        if word > 9999:
          messagebox.showerror(f"\"{line}\" is not valid instruction")
          return

        old_instructions.append(word)
      except ValueError:
        messagebox.showerror(f"\"{line}\" is not valid instruction")
        return

  for instruction in old_instructions:
    opcode, operand = divmod(instruction, 100) # Extract opcode and operand

    new_instructions.append((opcode * 1000) + operand) # Recombine opcode and operand in the new format


  with open(program_file_name, "w") as program_file:
    print(new_instructions)
    for word in new_instructions:
      program_file.write(f"{str(word)}\n")


def main(args):
  if len(args) < 2:
    print("Too few arguments.")
  elif len(args) > 2:
    print("Too many arguments.")
  convert_program_format(args[1])

if __name__ == '__main__':
  import sys
  sys.exit(main(sys.argv))
