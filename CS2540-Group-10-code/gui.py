import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox, simpledialog
from tkinter.colorchooser import askcolor
import configparser
from computer import Memory, CPU

class MainWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        # Load configuration for colors
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        # Set default options based on configuration
        self.master.option_add('*foreground', self.config['window']['foreground'])
        self.master.option_add('*background', self.config['window']['background'])
        self.master.option_add('*Button.foreground', self.config['button']['foreground'])
        self.master.option_add('*Button.background', self.config['button']['background'])

        self.pack(fill=tk.BOTH, expand=True)

        # Top button frame for Load, Save, and Change Color
        top_button_frame = tk.Frame(self)
        top_button_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

        load_program_button = tk.Button(top_button_frame, text="Load Program", command=self.load_program)
        save_program_button = tk.Button(top_button_frame, text="Save Program", command=self.save_program)
        change_color_button = tk.Button(top_button_frame, text="Change Color", command=self.change_color)
        load_program_button.pack(side=tk.LEFT, padx=5)
        save_program_button.pack(side=tk.LEFT, padx=5)
        change_color_button.pack(side=tk.LEFT, padx=5)

        # Frame for the Execute button below the load/save/change color buttons
        execute_button_frame = tk.Frame(self)
        execute_button_frame.pack(side=tk.TOP, fill=tk.X, pady=5)
        execute_program_button = tk.Button(execute_button_frame, text="Execute Program", command=self.execute_program)
        execute_program_button.pack(padx=5)

        # Text Editor for direct command editing
        self.text_editor = tk.Text(self, width=50, height=20)
        self.text_editor.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def load_program(self):
        """Loads a program file and displays its content in the text editor."""
        program_file_name = askopenfilename(title="Select Program File")
        if not program_file_name:
            return
        try:
            with open(program_file_name, 'r') as program_file:
                content = program_file.read()
            self.text_editor.delete("1.0", tk.END)
            self.text_editor.insert("1.0", content)
        except FileNotFoundError:
            messagebox.showerror("Error", "Program file not found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def save_program(self):
        """Saves the current program from the text editor to a file, with validation."""
        file_path = asksaveasfilename(title="Save Program As", defaultextension=".txt",
                                      filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if not file_path:
            return

        content = self.text_editor.get("1.0", tk.END).strip()
        lines = content.split("\n")
        validated_instructions = []

        for line in lines:
            line = line.strip()
            if line and line.lstrip('+-').isdigit():
                validated_instructions.append(line)
            else:
                messagebox.showerror("Error", f"Invalid instruction found: '{line}'. Fix it before saving.")
                return

        if len(validated_instructions) > 100:
            messagebox.showerror("Error", "Program exceeds the maximum size of 100 instructions.")
            return

        try:
            with open(file_path, 'w') as f:
                for instr in validated_instructions:
                    f.write(f"{instr}\n")
            messagebox.showinfo("Success", "Program saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save program: {e}")

    def change_color(self):
        """Opens a new window to select colors for various UI elements."""
        color_window = tk.Toplevel(self)
        color_window.title("Change Colors")
        tk.Label(color_window, text="Select which color to change:").pack(padx=10, pady=10)
        tk.Button(color_window, text="Window Foreground", command=self.select_window_foreground).pack(padx=5, pady=5)
        tk.Button(color_window, text="Window Background", command=self.select_window_background).pack(padx=5, pady=5)
        tk.Button(color_window, text="Button Foreground", command=self.select_button_foreground).pack(padx=5, pady=5)
        tk.Button(color_window, text="Button Background", command=self.select_button_background).pack(padx=5, pady=5)

    def execute_program(self):
        """Loads instructions from the text editor into memory and runs the CPU."""
        content = self.text_editor.get("1.0", tk.END).strip()
        lines = content.split("\n")

        try:
            instructions = [int(line.strip()) for line in lines if line.strip()]
            if len(instructions) > 100:
                messagebox.showerror("Error", "Program exceeds the maximum size of 100 instructions.")
                return

            memory = Memory()
            cpu = CPU(memory, self.open_output_window, self.open_input_window)

            for i, instr in enumerate(instructions):
                memory.set(i, instr)

            cpu.execute()
        except ValueError:
            messagebox.showerror("Error", "Program contains invalid instructions. Please check before executing.")
        except Exception as e:
            messagebox.showerror("Execution Error", f"An error occurred during execution: {e}")

    def open_output_window(self, output):
        """Displays output messages."""
        messagebox.showinfo("Output", output)

    def open_input_window(self, prompt):
        """Prompts the user for input during execution."""
        return simpledialog.askstring("Input", prompt)

    def select_window_foreground(self):
        chosen = askcolor()[1]
        if chosen:
            self.config['window']['foreground'] = chosen
            with open('config.ini', 'w') as config_file:
                self.config.write(config_file)
            self.master.option_add('*foreground', chosen)

    def select_window_background(self):
        chosen = askcolor()[1]
        if chosen:
            self.config['window']['background'] = chosen
            with open('config.ini', 'w') as config_file:
                self.config.write(config_file)
            self.master.option_add('*background', chosen)

    def select_button_foreground(self):
        chosen = askcolor()[1]
        if chosen:
            self.config['button']['foreground'] = chosen
            with open('config.ini', 'w') as config_file:
                self.config.write(config_file)
            self.master.option_add('*Button.foreground', chosen)

    def select_button_background(self):
        chosen = askcolor()[1]
        if chosen:
            self.config['button']['background'] = chosen
            with open('config.ini', 'w') as config_file:
                self.config.write(config_file)
            self.master.option_add('*Button.background', chosen)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Program Editor")
    app = MainWindow(root)
    root.mainloop()
