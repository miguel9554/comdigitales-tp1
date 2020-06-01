import numpy as np
import matplotlib.pyplot as plt

d = 2
M = 16

X = [d*(n-(M-1)/2) for n in range(M)]
Y = np.zeros(len(X))

fig, ax = plt.subplots()
ax.scatter(X, Y)
ax.spines['bottom'].set_position('center')
ax.spines['top'].set_color('none')
ax.spines['left'].set_color('none')
ax.spines['right'].set_color('none')
plt.yticks([])
plt.title('PAM 16')

plt.savefig('results/PAM.png')
