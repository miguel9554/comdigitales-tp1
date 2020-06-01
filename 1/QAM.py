import numpy as np
import matplotlib.pyplot as plt

d = 2
M = 16

X = d*[-1.5, -1.5, -1.5, -1.5, -0.5, -0.5, -0.5, -0.5, 1.5, 1.5, 1.5, 1.5, 0.5, 0.5, 0.5, 0.5]
Y = d*[1.5, 0.5, -0.5, -1.5, 1.5, 0.5, -0.5, -1.5, 1.5, 0.5, -0.5, -1.5, 1.5, 0.5, -0.5, -1.5]

fig, ax = plt.subplots()
ax.scatter(X, Y)
plt.title('QAM 16')
plt.savefig('results/QAM.png')
plt.show()
