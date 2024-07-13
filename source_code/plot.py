import matplotlib.pyplot as plt

time = [0, 1, 2, 3]
position = [0, 100, 200, 300]

plt.plot(time, position)
plt.xlabel('Time (hr)')
plt.ylabel('Position (km)')

# plt.show()

time = [0, 1, 2, 3]
position = [0, 10, 200, 300]

plt.plot(time, position)
plt.xlabel('Time (hr)')
plt.ylabel('Position (km)')

plt.show()

print("done")