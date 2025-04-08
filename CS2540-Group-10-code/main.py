import tkinter as tk

from gui import MainWindow

def main():

    root = tk.Tk()
    main_window = MainWindow(root)
    main_window.mainloop()
    

if __name__ == "__main__":
    main()
