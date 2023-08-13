counter_a = 0
count_b = 0
count_c = 0
count_d = 0
count_e = 0
count_f = 0
count_g = 0

inp = input("enter the alphabets : ")
alphabets = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
for i in inp:
    if i == 'a':
        counter_a += 1
    if i == 'b':
        count_b += 1
    if i == 'c':
        count_c += 1
    if i == 'd':
        count_d += 1
    if i == 'e':
        count_e += 1
    if i == 'f':
        count_f += 1
    if i == 'g':
        count_g += 1

print(f"{counter_a}a{count_b}b{count_c}c{count_d}d{count_e}e{count_f}f{count_g}")
