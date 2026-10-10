def prochitat_skript(put):
    stroki = []
    with open(put, "r", encoding="utf-8") as f:
        for stroka in f:
            stroka = stroka.strip()
            eto_komanda = stroka != "" and not stroka.startswith("#")
            if eto_komanda:
                stroki.append(stroka)
    return stroki