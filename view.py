with open("record.txt", "r") as file:
    data = file.readlines()

print("記録件数:", len(data))
print()

for line in data:
    print(line)
    