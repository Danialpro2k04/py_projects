import math
x = int(input("number: "))

if x == (0 or 1):
    print("the number is o or 1")
elif x > 1:
    for i in range(2, int(math.sqrt(x)) + 1):
        prime = True
        if x % i == 0:
            prime = False
    if prime:
        print("the number is a prime")
    else:
        print("the number isnt prime")
else:
    print("didnt understand")
