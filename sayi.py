import math

sayi = 1234567
ters_sayi = 0

while sayi > 0:
    birler= sayi % 10

    ters_sayi = (ters_sayi * 10) + birler

    sayi //= 10

print(ters_sayi)