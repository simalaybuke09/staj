def ters_cevir(sayi: float) -> str:
    _temp_dizi = []
    sayi_uzunlugu = len(str(sayi))
    j = 0
    while sayi > 0 and (j != sayi_uzunlugu):
        kalan = sayi % 10
        _temp_dizi.append(kalan)
        sayi //= 10
        j+=1

    result = "".join([str(i) for i in _temp_dizi])
    print(result)
    return  result


ters_cevir(12345067890)