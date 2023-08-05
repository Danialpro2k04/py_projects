import random

alphabets = "abcdefghijklmnopqrstuvwxyz"
capital_alphabets = alphabets.upper()
lower_alphabets = alphabets.lower()
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
special_set = ["!", "@", "#", "&"]

special_char = list(random.choices(special_set, k=2))
selected_nums = list(random.choices(nums, k=4))
alphas_cap = list(random.choices(capital_alphabets, k=2))
alphas_low = list(random.choices(lower_alphabets, k=8))


def create_pass(signs, numbers, alpha_capital, alpha_small):
    password = ""
    s = signs + numbers + alpha_capital + alpha_small
    random.shuffle(s)
    for i in s:
        password += str(i)
    return f"required strong password:  {password}"


print(create_pass(special_char, selected_nums, alphas_cap, alphas_low))
