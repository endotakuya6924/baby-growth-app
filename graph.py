import matplotlib.pyplot as plt

dates = []
weights = []

with open("record.txt", "r") as file:
    for line in file:
        date, name, weight = line.strip().split(",")
        dates.append(date)
        weights.append(int(weight))

plt.plot(dates, weights, marker="o")
plt.title("Baby Growth")
plt.xlabel("Date")
plt.ylabel("Weight (g)")
plt.show()