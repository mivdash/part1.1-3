import argparse

def razobrat_parametry():
    parser = argparse.ArgumentParser() # создание объекта парсера
    parser.add_argument("--vfs-path", dest="vfs_path", default=None) # ожидаем параметр с таким именем, но если его не указали то значение пустое
    parser.add_argument("--script", dest="script", default=None)
    return parser.parse_args() # функция берет то что идет после мейна и возвращает объект с полями выше