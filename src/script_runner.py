def prochitat_skript(put):
    stroki = []
    with open(put, "r", encoding="utf-8") as f: # правильное чтение букв
        for stroka in f:
            stroka = stroka.strip()
            eto_nuzhnaya_stroka = (stroka != "") and (not stroka.startswith("#"))
            if eto_nuzhnaya_stroka:
                stroki.append(stroka)
    return stroki