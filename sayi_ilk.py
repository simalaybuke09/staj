import math

sayi = 1234567
dizi = []
i=1

while True:
    kalan = (sayi % (10 ** i)) // (10 ** (i - 1)) 

    if  kalan == 0: #10 ** (i - 1) > sayi "sayida 0 da varsa uzunluk kontrolü"
            break
    
    dizi.append(kalan)

    i +=1
    
print(*dizi)
        


kalan = sayi // 10