import tkinter as tk # для отрисовки окон, кнопок, полей
import getpass # узнает имя пользователя для заголовка
import socket # узнать имя компютера для заголовка
from src.parser import razobrat_komandu
from src.vfs import sohranit_vfs # сохранить VFS из памяти на диск

class Prilojenie:
    def __init__(self, okno, vfs=None):
        self.okno = okno
        self.vfs = vfs  # дерево виртуальной файловой системы в памяти (или None, если не загружена)
        self._nastroit_zagolovok()
        self._sozdat_elementy()

    def _nastroit_zagolovok(self):
        polzovatel = getpass.getuser()
        imya_hosta = socket.gethostname()
        self.okno.title(f"Emulyator-[{polzovatel}@{imya_hosta}]")

    def _sozdat_elementy(self):
        self.oblast_vyvoda = tk.Text(self.okno, state=tk.DISABLED) # окно многострочное для чтения
        self.oblast_vyvoda.pack(fill=tk.BOTH, expand=True) # расположить виджеты друг под другом , растянуть и занять всё свободное место

        self.stroka_vvoda = tk.Entry(self.okno) #  окно для ввода односточное
        self.stroka_vvoda.pack(fill=tk.X) #растяжка по ширине
        self.stroka_vvoda.bind("<Return>", self._pri_nazhatii_enter) # приявзка ввода к функции


    def _vyvesti(self, tekst):
        self.oblast_vyvoda.config(state=tk.NORMAL)
        self.oblast_vyvoda.insert(tk.END, tekst + "\n") # вставляем текст в конец
        self.oblast_vyvoda.config(state=tk.DISABLED)
        self.oblast_vyvoda.see(tk.END)

    def _pri_nazhatii_enter(self, event):
        stroka_komandy = self.stroka_vvoda.get()
        self.stroka_vvoda.delete(0, tk.END)
        self._obrabotat(stroka_komandy)

    def _obrabotat(self, stroka_komandy):
        self._vyvesti(f"> {stroka_komandy}")
        tokeny = razobrat_komandu(stroka_komandy)
        if not tokeny:
            return

        komanda = tokeny[0]
        argumenty = tokeny[1:]

        if komanda == "exit":
            self.okno.destroy()
        elif komanda == "ls":
            self._vyvesti(f"ls stub: args={argumenty}")
        elif komanda == "cd":
            self._vyvesti(f"cd stub: args={argumenty}")
        elif komanda == "vfs-save":
            if not self.vfs:
                self._vyvesti("Error: VFS not loaded (use --vfs-path)")
            elif not argumenty:
                self._vyvesti("Error: vfs-save requires a path")
            else:
                sohranit_vfs(self.vfs, argumenty[0])
                self._vyvesti(f"VFS saved to {argumenty[0]}")
        else:
            self._vyvesti(f"Error: unknown command '{komanda}'")