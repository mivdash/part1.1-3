import shlex # разбивает строку на слова , если разделены пробелом то неразделяютс пробелом ещё

def razobrat_komandu(text):
    if not text.strip():
        return []
    try:
        return shlex.split(text)
    except ValueError:
        return text.split()