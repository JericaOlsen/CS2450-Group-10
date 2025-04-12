import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox, simpledialog
from tkinter.colorchooser import askcolor
import configparser
import re
import legacy_conversion  # import legacy conversion module
from computer import Memory, CPU

class MainWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        # Load configuration for colors.
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        # Set default options based on configuration.
        self.master.option_add('*foreground', self.config['window']['foreground'])
        self.master.option_add('*background', self.config['window']['background'])
        self.master.option_add('*Button.foreground', self.config['button']['foreground'])
        self.master.option_add('*Button.background', self.config['button']['background'])

        self.pack(fill=tk.BOTH, expand=True)

        # Top button frame for Load, Save, New Program, and Change Color.
        top_button_frame = tk.Frame(self)
        top_button_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

        load_program_button = tk.Button(top_button_frame, text="Load Program", command=self.load_program)
        new_program_button = tk.Button(top_button_frame, text="New Program", command=self.new_program)
        save_program_button = tk.Button(top_button_frame, text="Save Program", command=self.save_program)
        change_color_button = tk.Button(top_button_frame, text="Change Color", command=self.change_color)

        load_program_button.pack(side=tk.LEFT, padx=5)
        save_program_button.pack(side=tk.LEFT, padx=5)
        change_color_button.pack(side=tk.LEFT, padx=5)
        new_program_button.pack(side=tk.LEFT, padx=5)

        # Frame for the Execute button.
        execute_button_frame = tk.Frame(self)
        execute_button_frame.pack(side=tk.TOP, fill=tk.X, pady=5)
        execute_program_button = tk.Button(execute_button_frame, text="Execute Program", command=self.execute_program)
        execute_program_button.pack(padx=5)

        # Create the text editor and force removal of the default paste commands.
        self.text_editor = tk.Text(self, width=50, height=20)
        self.text_editor.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        # Unbind the default paste events.
        self.text_editor.unbind("<<Paste>>")
        self.text_editor.unbind("<Control-v>")
        self.text_editor.unbind("<Control-V>")
        # Bind our custom paste handler.
        self.text_editor.bind("<<Paste>>", self.handle_paste)
        self.text_editor.bind("<Control-v>", self.handle_paste)
        self.text_editor.bind("<Control-V>", self.handle_paste)
        # Bind the Return (Enter) key to a custom handler to prevent exceeding 250 lines.
        self.text_editor.bind("<Return>", self.handle_return)

    def new_program(self):
        new_window = tk.Toplevel(self.master)
        new_window.title("New Program")
        MainWindow(new_window)

    def handle_paste(self, event):
        """Custom paste handler that prevents pasting if it would exceed Memory.MAX_LINES."""
        try:
            clipboard = self.master.clipboard_get()
        except Exception:
            return "break"

        # Get the current text without the extra newline at the end.
        current_text = self.text_editor.get("1.0", "end-1c")
        current_lines = current_text.splitlines()
        current_line_count = len(current_lines)

        # Get the clipboard text lines.
        paste_lines = clipboard.splitlines()
        paste_line_count = len(paste_lines)

        # If a selection exists, those lines will be replaced.
        try:
            selection = self.text_editor.get("sel.first", "sel.last")
            selection_line_count = len(selection.splitlines())
        except tk.TclError:
            selection_line_count = 0

        effective_line_count = current_line_count - selection_line_count + paste_line_count

        if effective_line_count > Memory.MAX_LINES:
            messagebox.showerror(
                "Error",
                f"Paste not allowed: This paste would result in {effective_line_count} lines, "
                f"exceeding the maximum of {Memory.MAX_LINES} lines."
            )
            return "break"
        else:
            # If there is a selection, delete it first.
            try:
                self.text_editor.delete("sel.first", "sel.last")
            except tk.TclError:
                pass
            # Insert the clipboard text.
            self.text_editor.insert("insert", clipboard)
            return "break"

    def handle_return(self, event):
        """Prevents insertion of a newline if it would exceed Memory.MAX_LINES."""
        # Get the current content without the trailing newline.
        current_text = self.text_editor.get("1.0", "end-1c")
        current_lines = current_text.splitlines()
        current_line_count = len(current_lines)

        # Count lines that would be removed if a selection is active.
        try:
            selection = self.text_editor.get("sel.first", "sel.last")
            selection_lines = selection.splitlines()
            selection_line_count = len(selection_lines)
        except tk.TclError:
            selection_line_count = 0

        # Inserting a newline adds one new line.
        effective_line_count = current_line_count - selection_line_count + 1

        if effective_line_count > Memory.MAX_LINES:
            messagebox.showerror(
                "Error",
                f"Cannot insert new line: Maximum of {Memory.MAX_LINES} lines reached."
            )
            return "break"
        # Otherwise, allow the insertion of the newline (default behavior).
        return None

    def load_program(self):
        program_file_name = askopenfilename(title="Select Program File")
        if not program_file_name:
            return

        try:
            with open(program_file_name, 'r') as program_file:
                lines = program_file.readlines()

            new_format_pattern = re.compile(r'^-?\d{6}$')
            is_new_format = True
            for line in lines:
                trimmed = line.strip()
                if trimmed == "":
                    continue
                if not new_format_pattern.fullmatch(trimmed):
                    is_new_format = False
                    break

            if not is_new_format:
                conversion_success = legacy_conversion.convert_program_format(program_file_name)
                if not conversion_success:
                    messagebox.showerror("Error", "Legacy conversion failed. Cannot load file.")
                    return
                with open(program_file_name, 'r') as program_file:
                    content = program_file.read()
            else:
                content = "".join(lines)

            self.text_editor.delete("1.0", tk.END)
            self.text_editor.insert("1.0", content)
        except FileNotFoundError:
            messagebox.showerror("Error", "Program file not found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def save_program(self):
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

        if len(validated_instructions) > Memory.MAX_LINES:
            messagebox.showerror("Error", f"Program exceeds the maximum size of {Memory.MAX_LINES} instructions.")
            return

        try:
            with open(file_path, 'w') as f:
                for instr in validated_instructions:
                    f.write(f"{instr}\n")
            messagebox.showinfo("Success", "Program saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save program: {e}")

    def change_color(self):
        color_window = tk.Toplevel(self)
        color_window.title("Change Colors")
        tk.Label(color_window, text="Select which color to change:").pack(padx=10, pady=10)
        tk.Button(color_window, text="Window Foreground", command=self.select_window_foreground).pack(padx=5, pady=5)
        tk.Button(color_window, text="Window Background", command=self.select_window_background).pack(padx=5, pady=5)
        tk.Button(color_window, text="Button Foreground", command=self.select_button_foreground).pack(padx=5, pady=5)
        tk.Button(color_window, text="Button Background", command=self.select_button_background).pack(padx=5, pady=5)

    def execute_program(self):
        content = self.text_editor.get("1.0", tk.END).strip()
        lines = content.split("\n")

        try:
            instructions = [int(line.strip()) for line in lines if line.strip()]
            if len(instructions) > Memory.MAX_LINES:
                messagebox.showerror("Error", f"Program exceeds the maximum size of {Memory.MAX_LINES} instructions.")
                return

            memory = Memory()
            cpu = CPU(memory, self.open_input_window, self.open_output_window)

            for i, instr in enumerate(instructions):
                memory.set(i, instr)

            cpu.execute()
        except ValueError:
            messagebox.showerror("Error", "Program contains invalid instructions. Please check before executing.")
        except Exception as e:
            messagebox.showerror("Execution Error", f"An error occurred during execution: {e}")

    def open_output_window(self, output):
        messagebox.showinfo("Output", output)

    def open_input_window(self, prompt):
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
