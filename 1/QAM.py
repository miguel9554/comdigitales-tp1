import numpy as np
import matplotlib.pyplot as plt

d = 2
d_aux = [2]
M = 16

X_aux = [-1.5, -1.5, -1.5, -1.5, -0.5, -0.5, -0.5, -0.5, 1.5, 1.5, 1.5, 1.5, 0.5, 0.5, 0.5, 0.5]
Y_aux = [1.5, 0.5, -0.5, -1.5, 1.5, 0.5, -0.5, -1.5, 1.5, 0.5, -0.5, -1.5, 1.5, 0.5, -0.5, -1.5]

X = np.multiply(d_aux,X_aux)
Y = np.multiply(d_aux,Y_aux)

#agrego fronteras de decision y codigo gray
xcoords = [-d, 0, d]
gray_code = ['0100', '0110', '1110', '1100', '0000', '0010', '1010', '1000', '0101', '0111', '1111', '1101','0001', '0011', '1011', '1001']

fig, ax = plt.subplots()
ax.scatter(X, Y)
for xc in xcoords:
    plt.axvline(x=xc,color='r',linestyle='dashed')
    plt.axhline(y=xc,color='r',linestyle='dashed')
    
for i, txt in enumerate(gray_code):
    ax.annotate(txt, (X[i], Y[i]))

plt.gca().set_aspect('equal', adjustable='box')
plt.title('QAM 16')
plt.savefig('results/QAM.png')
plt.show()
