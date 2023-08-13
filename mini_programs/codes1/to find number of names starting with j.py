x = ["john", "jon", "bones", "trevor", "scott", "ones"]
y = []
z = []
for name in x:
    if name.startswith("j"):
        y.append(name)
    else:
        z.append(name)

print(f"the number of words starting with j: {len(y)}")
print(f"the number of words starting without j: {len(z)}")
