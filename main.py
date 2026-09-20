import tkinter as tk
from src.gui import Prilojenie
from src.config import razobrat_parametry
from src.script_runner import prochitat_skript
from src.vfs import zagruzit_vfs

def glavnaya_funktsiya():
    parametry = razobrat_parametry()

    print("Parametry zapuska:")
    print("  vfs-path =", parametry.vfs_path)
    print("  script =", parametry.script)

    vfs = None
    if parametry.vfs_path:
        vfs = zagruzit_vfs(parametry.vfs_path)
        print("VFS zagruzhena iz:", parametry.vfs_path)

    okno = tk.Tk()
    okno.geometry("600x400")
    app = Prilojenie(okno, vfs=vfs)

    if parametry.script:
        for stroka in prochitat_skript(parametry.script):
            app._obrabotat(stroka)
            if stroka.split()[0] == "exit":
                break

    okno.mainloop()

if __name__ == "__main__":
    glavnaya_funktsiya()