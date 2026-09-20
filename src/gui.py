import tkinter as tk # для отрисовки окон, кнопок, полей
import getpass # узнает имя пользователя для заголовка
import socket # узнать имя компютера для заголовка
import time # для команды uptime - сколько времени работает эмулятор
from src.parser import razobrat_komandu
from src.vfs import sohranit_vfs # сохранить VFS из памяти на диск

class Prilojenie:
    def __init__(self, okno, vfs=None):
        self.okno = okno
        self.vfs = vfs  # корень дерева виртуальной файловой системы в памяти (или None, если не загружена)
        self.tekuschiy_put = []  # список имён папок от корня до текущей папки, например ["docs", "2024"]
        self.vremya_starta = time.time()  # момент запуска эмулятора, для команды uptime
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

    def _naiti_uzel(self, put_spisok):
        """Найти узел дерева VFS, идя от корня по списку имён папок."""
        uzel = self.vfs
        for imya in put_spisok:
            if uzel is None or uzel["tip"] != "papka":
                return None
            naiden = None
            for rebenok in uzel["deti"]:
                if rebenok["imya"] == imya:
                    naiden = rebenok
                    break
            if naiden is None:
                return None
            uzel = naiden
        return uzel

    def _komanda_ls(self, argumenty):
        if not self.vfs:
            self._vyvesti("Error: VFS not loaded (use --vfs-path)")
            return

        if argumenty:
            tselevoy_put = self.tekuschiy_put + [argumenty[0]]
        else:
            tselevoy_put = self.tekuschiy_put

        uzel = self._naiti_uzel(tselevoy_put)

        if uzel is None:
            self._vyvesti(f"ls: {argumenty[0] if argumenty else '.'}: no such file or directory")
        elif uzel["tip"] == "fayl":
            self._vyvesti(uzel["imya"])
        else:
            if not uzel["deti"]:
                self._vyvesti("(pusto)")
            for rebenok in uzel["deti"]:
                if rebenok["tip"] == "papka":
                    self._vyvesti(rebenok["imya"] + "/")
                else:
                    self._vyvesti(rebenok["imya"])

    def _komanda_cd(self, argumenty):
        if not self.vfs:
            self._vyvesti("Error: VFS not loaded (use --vfs-path)")
            return

        if not argumenty:
            self.tekuschiy_put = []
            return

        imya = argumenty[0]

        if imya == "..":
            if self.tekuschiy_put:
                self.tekuschiy_put = self.tekuschiy_put[:-1]
            return

        noviy_put = self.tekuschiy_put + [imya]
        uzel = self._naiti_uzel(noviy_put)

        if uzel is None:
            self._vyvesti(f"cd: {imya}: no such file or directory")
        elif uzel["tip"] != "papka":
            self._vyvesti(f"cd: {imya}: not a directory")
        else:
            self.tekuschiy_put = noviy_put
    def _komanda_rmdir(self, argumenty):
        if not self.vfs:
            self._vyvesti("Error: VFS not loaded (use --vfs-path)")
            return

        if not argumenty:
            self._vyvesti("Error: rmdir requires a name")
            return

        imya = argumenty[0]
        tekuschaya_papka = self._naiti_uzel(self.tekuschiy_put)

        naiden = None
        for rebenok in tekuschaya_papka["deti"]:
            if rebenok["imya"] == imya:
                naiden = rebenok
                break

        if naiden is None:
            self._vyvesti(f"rmdir: {imya}: no such file or directory")
        elif naiden["tip"] != "papka":
            self._vyvesti(f"rmdir: {imya}: not a directory")
        elif naiden["deti"]:
            self._vyvesti(f"rmdir: {imya}: directory not empty")
        else:
            tekuschaya_papka["deti"].remove(naiden)
            self._vyvesti(f"rmdir: {imya} removed")

    def _komanda_uptime(self):
        proshlo_sekund = time.time() - self.vremya_starta
        self._vyvesti(f"uptime: {int(proshlo_sekund)} sec")

    def _komanda_clear(self):
        self.oblast_vyvoda.config(state=tk.NORMAL)
        self.oblast_vyvoda.delete("1.0", tk.END)
        self.oblast_vyvoda.config(state=tk.DISABLED)

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
            self._komanda_ls(argumenty)
        elif komanda == "cd":
            self._komanda_cd(argumenty)
        elif komanda == "uptime":
            self._komanda_uptime()
        elif komanda == "clear":
            self._komanda_clear()
        elif komanda == "echo":
            self._vyvesti(" ".join(argumenty))
        elif komanda == "rmdir":
            self._komanda_rmdir(argumenty)
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