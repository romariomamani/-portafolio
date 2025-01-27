import matplotlib.pyplot as plt
import numpy as np

# Problema 3
x = np.linspace(0, 12, 400)
y1 = 12 - x
y2 = np.full_like(x, 6)
y3 = np.full_like(x, 4)

plt.figure(figsize=(10, 6))
plt.plot(x, y1, label='x + y = 12')
plt.plot(x, y2, label='y = 6')
plt.plot(y3, x, label='x = 4')
plt.fill_between(x, 0, y1, where=(x >= 4) & (y1 >= 6), color='gray', alpha=0.5)
plt.xlim(0, 12)
plt.ylim(0, 12)
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.title('Problema 3')
plt.savefig('problema3.png')  # Guardar la gráfica como imagen
plt.close()

# Problema 4
P1 = np.linspace(0, 9, 400)
P2 = (18 - 2 * P1) / 3

plt.figure(figsize=(10, 6))
plt.plot(P1, P2, label='2P1 + 3P2 = 18')
plt.fill_between(P1, 0, P2, where=(P1 >= 0) & (P2 >= 0), color='gray', alpha=0.5)
plt.xlim(0, 9)
plt.ylim(0, 6)
plt.xlabel('P1')
plt.ylabel('P2')
plt.legend()
plt.title('Problema 4')
plt.savefig('problema4.png')  # Guardar la gráfica como imagen
plt.close()

# Problema 5
A = np.linspace(0, 10, 400)
B = (50 - 5 * A) / 10

plt.figure(figsize=(10, 6))
plt.plot(A, B, label='5A + 10B = 50')
plt.fill_between(A, 0, B, where=(A >= 0) & (B >= 0), color='gray', alpha=0.5)
plt.xlim(0, 10)
plt.ylim(0, 5)
plt.xlabel('A')
plt.ylabel('B')
plt.legend()
plt.title('Problema 5')
plt.savefig('problema5.png')  # Guardar la gráfica como imagen
plt.close()
