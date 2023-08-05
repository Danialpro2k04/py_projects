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

password = special_char + selected_nums + alphas_cap + alphas_low
random.shuffle(password)

resulted_pass = ""
for i in password:
    resulted_pass += str(i)

print("Random strong password: " + resulted_pass)
