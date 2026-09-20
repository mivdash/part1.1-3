import os

def zagruzit_vfs(put):
    imya = os.path.basename(put.rstrip("/\\")) or put

    if os.path.isdir(put):
        deti = []
        for element in os.listdir(put):
            polny_put = os.path.join(put, element)
            deti.append(zagruzit_vfs(polny_put))
        return {"imya": imya, "tip": "papka", "deti": deti}
    else:
        with open(put, "rb") as f:
            dannye = f.read()
        return {"imya": imya, "tip": "fayl", "soderzhimoe": dannye}


def sohranit_vfs(uzel, put):
    if uzel["tip"] == "papka":
        os.makedirs(put, exist_ok=True)
        for rebenok in uzel["deti"]:
            noviy_put = os.path.join(put, rebenok["imya"])
            sohranit_vfs(rebenok, noviy_put)
    else:
        with open(put, "wb") as f:
            f.write(uzel["soderzhimoe"])