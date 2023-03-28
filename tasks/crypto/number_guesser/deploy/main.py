#!/usr/local/bin/python3
from Crypto.Util.number import getPrime
from Crypto.Random.random import randint

q = getPrime(512)
p = getPrime(512)
n = p * q

value = randint(1, n)

used_oracle = False

print(p)
print(q)

print("Китайский шайтан-машын преведсдвкует тебя")
print("Моя уметь отвечать на вопросы. Адын вапрос про модуль числа по основанию, адын на угадайку.")
while True:
    print("Што ты от меня хотеть?")
    print("1: Модуль по числу")
    print("2: Угадать число")
    print("3: Ухади")

    s = input(">> ")

    if s == "1":
        if used_oracle:
            print("Ууу, шайтан-машын не проведешь! Адин раз спросить можно!")
            print()
        else:
            modulus = input("Давай свой модуль-шайтан: ")
            modulus = int(modulus)
            if modulus <= 0:
                print("Ээээ пазитивный давай!")
                print()
            else:
                used_oracle = True
                print(value % modulus)
                print()
    elif s == "2":
        check = input("Попробуй угадай: ")
        if int(check) == value:
            print("vrnctf{b1g1nt_fort9ne_tell3r}")
        else:
            print("Хе-хе, не угадаль")
        exit()
    else:
        print("Захади еще, дарагой")
        exit()
