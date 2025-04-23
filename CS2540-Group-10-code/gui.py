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

        # maximums
        self.LINE_LIMIT = 250   # total lines
        self.CHAR_LIMIT = 7     # max characters per line
        self.WORD_LIMIT = 250   # (optional) still enforce word limit on paste

        # Load configuration for colors.
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        # Apply colors
        self.master.option_add('*foreground', self.config['window']['foreground'])
        self.master.option_add('*background', self.config['window']['background'])
        self.master.option_add('*Button.foreground', self.config['button']['foreground'])
        self.master.option_add('*Button.background', self.config['button']['background'])

        self.pack(fill=tk.BOTH, expand=True)

        # Buttons frame
        top_button_frame = tk.Frame(self)
        top_button_frame.pack(side=tk.TOP, fill=tk.X, pady=5)
        tk.Button(top_button_frame, text="Load Program", command=self.load_program).pack(side=tk.LEFT, padx=5)
        tk.Button(top_button_frame, text="Save Program", command=self.save_program).pack(side=tk.LEFT, padx=5)
        tk.Button(top_button_frame, text="Change Color", command=self.change_color).pack(side=tk.LEFT, padx=5)
        tk.Button(top_button_frame, text="New Program",  command=self.new_program).pack(side=tk.LEFT, padx=5)

        # Execute button
        execute_frame = tk.Frame(self)
        execute_frame.pack(side=tk.TOP, fill=tk.X, pady=5)
        tk.Button(execute_frame, text="Execute Program", command=self.execute_program).pack(padx=5)

        # Text editor
        self.text_editor = tk.Text(self, width=50, height=20)
        self.text_editor.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Override paste
        for seq in ("<<Paste>>", "<Control-v>", "<Control-V>"):
            self.text_editor.unbind(seq)
            self.text_editor.bind(seq, self.handle_paste)

        # Prevent too many lines on Enter
        self.text_editor.bind("<Return>", self.handle_return)
        # Prevent too many chars per line on typing
        self.text_editor.bind("<Key>", self.handle_key)

    def new_program(self):
        new_window = tk.Toplevel(self.master)
        new_window.title("New Program")
        MainWindow(new_window)

    def handle_key(self, event):
        """Prevent any line from exceeding CHAR_LIMIT characters."""
        # Allow navigation/control keys
        if event.keysym in (
            'BackSpace','Left','Right','Up','Down','Delete',
            'Return','Home','End','Tab','Shift_L','Shift_R',
            'Control_L','Control_R','Alt_L','Alt_R'
        ):
            return None

        char = event.char
        # Only intercept printable chars
        if not char or ord(char) < 32:
            return None

        # Determine current line text (before insertion)
        line_start = self.text_editor.index("insert linestart")
        line_end   = self.text_editor.index("insert lineend")
        current_line = self.text_editor.get(line_start, line_end)

        if len(current_line) + 1 > self.CHAR_LIMIT:
            messagebox.showerror(
                "Line Too Long",
                f"Lines may have at most {self.CHAR_LIMIT} characters."
            )
            return "break"

        return None  # allow insertion

    def handle_paste(self, event):
        """Prevent pasting if it violates line count or char-per-line limits."""
        try:
            clip = self.master.clipboard_get()
        except Exception:
            return "break"

        existing = self.text_editor.get("1.0", "end-1c")
        lines    = existing.splitlines()

        # Selection to be replaced
        try:
            sel = self.text_editor.get("sel.first", "sel.last")
            sel_lines = sel.splitlines()
            sel_words = sel.split()
        except tk.TclError:
            sel_lines = []
            sel_words = []

        clip_lines = clip.splitlines()
        clip_words = clip.split()

        # Check total lines
        new_line_count = len(lines) - len(sel_lines) + len(clip_lines)
        if new_line_count > self.LINE_LIMIT:
            messagebox.showerror(
                "Line Limit Exceeded",
                f"Pasting would create {new_line_count} lines (max {self.LINE_LIMIT})."
            )
            return "break"

        # Check per-line length
        for ln in clip_lines:
            if len(ln) > self.CHAR_LIMIT:
                messagebox.showerror(
                    "Paste Error",
                    f"Line '{ln}' has {len(ln)} chars (max {self.CHAR_LIMIT})."
                )
                return "break"

        existing_words = existing.split()
        new_word_count = len(existing_words) - len(sel_words) + len(clip_words)
        if new_word_count > self.WORD_LIMIT:
            messagebox.showerror(
                "Word Limit Exceeded",
                f"Pasting would create {new_word_count} words (max {self.WORD_LIMIT})."
            )
            return "break"

        # Perform paste
        try:
            self.text_editor.delete("sel.first", "sel.last")
        except tk.TclError:
            pass
        self.text_editor.insert("insert", clip)
        return "break"

    def handle_return(self, event):
        """Prevent adding lines beyond LINE_LIMIT."""
        existing = self.text_editor.get("1.0", "end-1c")
        lines = existing.splitlines()
        try:
            sel = self.text_editor.get("sel.first", "sel.last")
            sel_count = len(sel.splitlines())
        except tk.TclError:
            sel_count = 0

        if len(lines) - sel_count + 1 > self.LINE_LIMIT:
            messagebox.showerror(
                "Line Limit Reached",
                f"Cannot exceed {self.LINE_LIMIT} lines."
            )
            return "break"
        return None

    def load_program(self):
        fname = askopenfilename(title="Select Program File")
        if not fname:
            return

        try:
            with open(fname, 'r') as f:
                raw_lines = f.readlines()

            # Enforce total line count on load
            if len(raw_lines) > self.LINE_LIMIT:
                messagebox.showerror(
                    "Error",
                    f"File has {len(raw_lines)} lines, exceeds max of {self.LINE_LIMIT}."
                )
                return

            # Enforce per-line char limit on load
            for i, ln in enumerate(raw_lines, 1):
                if len(ln.rstrip('\n')) > self.CHAR_LIMIT:
                    messagebox.showerror(
                        "Error",
                        f"Line {i} has {len(ln.rstrip())} chars (max {self.CHAR_LIMIT})."
                    )
                    return

            # Detect new vs legacy format
            new_fmt = re.compile(r'^-?\d{6}$')
            is_new = all(
                (not ln.strip()) or new_fmt.fullmatch(ln.strip())
                for ln in raw_lines
            )

            if not is_new:
                ok = legacy_conversion.convert_program_format(fname)
                if not ok:
                    messagebox.showerror("Error", "Legacy conversion failed.")
                    return
                with open(fname, 'r') as f:
                    content = f.read()
            else:
                content = "".join(raw_lines)

            self.text_editor.delete("1.0", tk.END)
            self.text_editor.insert("1.0", content)

        except FileNotFoundError:
            messagebox.showerror("Error", "File not found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def save_program(self):
        file_path = asksaveasfilename(
            title="Save Program As",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not file_path:
            return

        content = self.text_editor.get("1.0", "end-1c").strip()
        lines   = content.split("\n")

        # Validate each line
        validated = []
        for i, ln in enumerate(lines, 1):
            if len(ln) > self.CHAR_LIMIT:
                messagebox.showerror(
                    "Error",
                    f"Line {i} has {len(ln)} chars (max {self.CHAR_LIMIT})."
                )
                return
            stripped = ln.strip()
            if stripped and stripped.lstrip('+-').isdigit():
                validated.append(stripped)
            else:
                messagebox.showerror("Error", f"Invalid instruction on line {i}: '{ln}'")
                return

        if len(validated) > self.LINE_LIMIT:
            messagebox.showerror(
                "Error",
                f"Program exceeds {self.LINE_LIMIT} instructions."
            )
            return

        try:
            with open(file_path, 'w') as f:
                for instr in validated:
                    f.write(instr + "\n")
            messagebox.showinfo("Success", "Program saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Save failed: {e}")

    def change_color(self):
        win = tk.Toplevel(self)
        win.title("Change Colors")
        tk.Label(win, text="Pick a color to change:").pack(padx=10, pady=10)
        tk.Button(win, text="Window FG", command=self.select_window_foreground).pack(pady=2)
        tk.Button(win, text="Window BG", command=self.select_window_background).pack(pady=2)
        tk.Button(win, text="Button FG", command=self.select_button_foreground).pack(pady=2)
        tk.Button(win, text="Button BG", command=self.select_button_background).pack(pady=2)
        tk.Button(win, text="Save Colors", command=self.save_colors).pack(pady=5)

    def select_window_foreground(self):
        c = askcolor()[1]
        if c: self.config['window']['foreground'] = c

    def select_window_background(self):
        c = askcolor()[1]
        if c: self.config['window']['background'] = c

    def select_button_foreground(self):
        c = askcolor()[1]
        if c: self.config['button']['foreground'] = c

    def select_button_background(self):
        c = askcolor()[1]
        if c: self.config['button']['background'] = c

    def save_colors(self):
        with open('config.ini', 'w') as cfg:
            self.config.write(cfg)
        self.master.option_add('*foreground', self.config['window']['foreground'])
        self.master.option_add('*background', self.config['window']['background'])
        self.master.option_add('*Button.foreground', self.config['button']['foreground'])
        self.master.option_add('*Button.background', self.config['button']['background'])

    def execute_program(self):
        content = self.text_editor.get("1.0", "end-1c").strip()
        lines   = [ln for ln in content.split("\n") if ln.strip()]

        try:
            if len(lines) > self.LINE_LIMIT:
                raise ValueError(f"Program exceeds {self.LINE_LIMIT} lines.")
            instructions = []
            for i, ln in enumerate(lines, 1):
                if len(ln) > self.CHAR_LIMIT:
                    raise ValueError(f"Line {i} > {self.CHAR_LIMIT} chars.")
                instructions.append(int(ln))
            memory = Memory()
            cpu    = CPU(memory, self.open_input_window, self.open_output_window)
            for idx, instr in enumerate(instructions):
                memory.set(idx, instr)
            cpu.execute()
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Execution Error", str(e))

    def open_output_window(self, output):
        messagebox.showinfo("Output", output)

    def open_input_window(self, prompt):
        return simpledialog.askstring("Input", prompt)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Program Editor")
    app = MainWindow(root)
    root.mainloop()
