# UVSim - Virtual Machine Simulator

## Source Control Link
[GitHub Repository](https://github.com/JericaOlsen/CS2450-Group-10)

## Overview

**UVSim** is a software-based virtual machine developed to help computer science students learn machine language and computer architecture. It enables students to execute machine language programs using a simple instruction set known as **BasicML**. This updated version includes several new enhancements in the user interface and program editing capabilities.

## Features

- **CPU Simulation:**
  - Simulates a CPU with an accumulator register and a control register.
  - Handles basic arithmetic, memory, and control (branch) operations.

- **Memory Simulation:**
  - Provides exactly **250 memory storage locations** (indexed from `000` to `249`).
  - Each memory location stores a signed six‑digit word (from ±000000 to ±999999).

- **Instruction Set Support:**
  - Supports a set of instructions including I/O operations, arithmetic calculations, load/store operations, and branching commands.

- **Integrated Text Editor:**
  - A built‑in editor allows you to directly edit BasicML instructions.
  - Pasting or editing operations are now limited so that the number of program lines never exceeds the 250 memory locations. If an operation would exceed the limit, it is prevented and an error message is shown.

- **Legacy Conversion:**
  - Automatically detects and converts legacy program files to the new six‑digit format when loading a file.

- **User Interface Enhancements:**
  - A new menu bar includes buttons for **Load Program**, **Save Program**, **New Program**, and **Change Color**.
  - The **Change Color** feature allows customization of the UI (window and button foreground/background colors) through a dedicated color selection window.

- **Interactive Execution:**
  - Real‑time execution feedback: Input and output dialog windows manage program interaction during execution.
  - Execution stops when a HALT instruction (`43`) is encountered, with error handling for issues such as division by zero and unknown opcodes.

## System Requirements

- **Operating System:** Windows, macOS, or Linux
- **Python Version:** Python 3.7 or higher (Python 3.10+ is recommended for the use of the `match`/`case` statement)
- **Memory:** At least 512MB of RAM
- **Storage:** At least 50MB of free disk space
- **Dependencies:**
  - Standard Python libraries
  - `pytest` is required for running tests (in addition to using built‑in modules like `unittest.mock`)

## System Components

### CPU (Central Processing Unit)
- **Accumulator:** Stores intermediate results during calculations.
- **Control Register (CR):** Points to the current instruction in memory.
- Operates on six‑digit words (±000000 to ±999999) with three‑digit memory addresses (000–249).

### Memory
- **Size:** 250-word memory (indexed from `000` to `249`).
- **Word Format:** Each location holds a six‑digit signed integer (e.g., `+123456` or `-654321`).

## Instruction Set (BasicML)

### I/O Operations

| Opcode | Instruction | Description                                                      |
|--------|-------------|------------------------------------------------------------------|
| `10`   | `READ`      | Read a word from the keyboard into a specified memory location.  |
| `11`   | `WRITE`     | Write a word from a specified memory location to the screen.     |

### Load/Store Operations

| Opcode | Instruction | Description                                                      |
|--------|-------------|------------------------------------------------------------------|
| `20`   | `LOAD`      | Load a word from a specified memory location into the accumulator.|
| `21`   | `STORE`     | Store the accumulator's value into a specified memory location.   |

### Arithmetic Operations

| Opcode | Instruction | Description                                                      |
|--------|-------------|------------------------------------------------------------------|
| `30`   | `ADD`       | Add a word from memory to the accumulator.                       |
| `31`   | `SUBTRACT`  | Subtract a word in memory from the accumulator.                  |
| `32`   | `DIVIDE`    | Divide the accumulator by a word from memory. (Handles division by zero) |
| `33`   | `MULTIPLY`  | Multiply the accumulator by a word from memory.                  |

### Control Operations

| Opcode | Instruction  | Description                                                      |
|--------|--------------|------------------------------------------------------------------|
| `40`   | `BRANCH`       | Unconditionally jump to a specified memory address.            |
| `41`   | `BRANCHNEG`    | Jump to a specified memory address if the accumulator is negative. |
| `42`   | `BRANCHZERO`   | Jump to a specified memory address if the accumulator is zero.   |
| `43`   | `HALT`         | Terminate program execution.                                     |

## Program Execution & Running UVSim

1. **Load the Program:**
   - Place your BasicML program in a text file (e.g., `program.txt`).
   - Click the **Load Program** button to import the file into the built‑in text editor.
   - If the loaded file is in a legacy format, UVSim automatically converts it to the new six‑digit format.

2. **Edit & Save:**
   - Directly edit your BasicML instructions in the text editor.
   - The editor prevents any paste or insertion that would exceed 250 lines (the maximum number of memory locations).
   - Click the **Save Program** button to save the validated instructions to a file.

3. **Execute:**
   - Click the **Execute Program** button to load the instructions into memory and run them sequentially from memory location `000`.
   - Execution continues until a HALT (`43`) instruction is encountered.

4. **Interactive I/O:**
   - During execution, UVSim prompts you for input (if required) and displays output using dialog windows.

5. **Customizing the UI:**
   - Use the **Change Color** button to open the color selection window.
   - Customize the window and button foreground/background colors according to your preference.

6. **New Program Window:**
   - The **New Program** button opens a separate editor window, allowing you to work on multiple programs concurrently.

## Configuration File

UVSim uses a configuration file (`config.ini`) to store UI color settings. Below is an example configuration file:

```ini
[window]
background = #FFFFFF
foreground = #000000

[button]
background = #4C721D
foreground = black
```

## Example Program (BasicML)

```plaintext
1007  # READ value into memory[07]
2007  # LOAD memory[07] into accumulator
3008  # ADD value at memory[08] to accumulator
2109  # STORE result in memory[09]
1109  # WRITE value at memory[09] to screen
4300  # HALT program execution
```

## Contributors

- Diego Martinez Cardenas
- Jerica Olsen
- Jared Brewer
