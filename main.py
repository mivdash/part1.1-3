import tkinter as tk
from src.gui import Prilojenie


def glavnaya_funktsiya():
    okno = tk.Tk()
    okno.geometry("600x400")
    Prilojenie(okno)
    okno.mainloop()


if __name__ == "__main__":
    glavnaya_funktsiya()