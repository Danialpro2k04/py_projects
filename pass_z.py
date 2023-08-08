import random

size = int(input("enter lenght of password(82 >=password >= 15): "))
raw = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%"

alphabets = "abcdefghijklmnopqrstuvwxyz"
capital_alphabets = alphabets.upper()
lower_alphabets = alphabets.lower()
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
special_set = ["!", "@", "#", "&"]

k_special = int(input("enter the least number of special: "))
k_numbers = int(input("enter the least amount of numbers in your password: "))
k_capitals = int(input("enter the least amount of upper case alphabets: "))
k_lowers = int(input("enter the least amount of lower case alphabets: "))
print("the remaining lenght of password will be created randomly")

sum = k_lowers + k_capitals + k_numbers + k_special

if sum <= size:
    s_specials = list(random.choices(special_set, k=k_special))
    s_nums = list(random.choices(nums, k=k_numbers))
    s_upper = list(random.choices(capital_alphabets, k=k_capitals))
    s_lower = list(random.choices(lower_alphabets, k=k_lowers))

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
else:
    print("the lesast numbers input should not be greater than given size of the password")

create_pass(s_specials, s_nums, s_lower, s_upper)
