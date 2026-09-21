import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.parser import razobrat_komandu
from src.vfs import zagruzit_vfs, sohranit_vfs

def check(condition, message):
    if not condition:
        raise AssertionError(message)
    print("OK:", message)

check(razobrat_komandu("ls -la") == ["ls", "-la"], "парсер разбивает по пробелам")
check(razobrat_komandu('cd "My Documents"') == ["cd", "My Documents"], "парсер понимает кавычки")
check(razobrat_komandu("") == [], "пустая строка даёт пустой список")

print("\nВсе проверки пройдены.")