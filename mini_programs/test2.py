import random

while True:
    pass_len = int(input("enter password lenght(lenght<67): \n"))
    raw_characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%"

    special_char = random.sample(raw_characters, pass_len)

    resulted_pass = ""
    for i in special_char:
        resulted_pass += str(i)

    print("Random strong password: " + resulted_pass)

    x = input("do you want to continue?(y/n)\n")
    if x == "y":
        continue
    elif x == "n":
        break
    else:
        print("i did not understand that")
        continue
