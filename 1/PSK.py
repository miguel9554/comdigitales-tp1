import numpy as np
import matplotlib.pyplot as plt

d = 2
M = 16

r = d/(2*np.sin(np.pi/M))
angles = [2*np.pi*(m-1)/M for m in range(1, M+1)]

X = [r*np.cos(angle) for angle in angles]
Y = [r*np.sin(angle) for angle in angles]

plt.scatter(X, Y)
plt.title('PSK 16')
plt.gca().set_aspect('equal', adjustable='box')


plt.savefig('results/PSK.png')
plt.show()
