import matplotlib.pyplot as plt

plt.interactive(False)
f = open("./test.txt", "r")
x, y = [], []
for line in f:
    if "PUT" in line:
        tmp1 = line.split(":")
        x.append(int(tmp1[0][7:]))
        y.append(float(tmp1[1][1:]))
plt.plot(x, y)
plt.show()
