import random

size = int(input("enter lenght of password(82 >=password >= 15): "))
raw = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%"

alphabets = "abcdefghijklmnopqrstuvwxyz"
capital_alphabets = alphabets.upper()
lower_alphabets = alphabets.lower()
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
special_set = ["!", "@", "#", "&"]

print('password will have atleast 3 capital letters, 5 lower letters, 3 special characters and 4 numbers')

s_specials = list(random.choices(special_set, k=3))
s_nums = list(random.choices(nums, k=4))
s_lower = list(random.choices(capital_alphabets, k=3))
s_upper = list(random.choices(lower_alphabets, k=5))


def create_pass(signs, numbers, alpha_capital, alpha_small):
    password = ""
    s = signs + numbers + alpha_capital + alpha_small
    random.shuffle(s)
    for i in s:
        password += str(i)

    if size > 15:
        n_size = size - 15
        pass_x = random.sample(raw, n_size)
        for z in pass_x:
            password += str(z)
        print(f"required strong password:  {password}")
        print(f"the lenght of password is {len(password)}")
    elif size == 15:
        print(f"required strong password:  {password}")
        print(f"the lenght of password is {len(password)}")
    else:
        print("size of password should be greater than or equal to 15")


create_pass(s_specials, s_nums, s_lower, s_upper)
