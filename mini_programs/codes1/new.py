print("********")
for i in reversed(range(7)):
    for j in range(7):
        if (i == j):
            print("*", end="")
        else:
            print(" ", end="")
    print("")
