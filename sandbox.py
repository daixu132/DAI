def dec2bin(value):
    ''' Return a list containing binary representation of passed integer.'''
 
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

print('Starting script...')

import numpy as np
import matplotlib.pyplot as plt

plt.axis([0, 10, 0, 1])

for i in range(10):
    y = np.random.random()
    plt.scatter(i, y)
    plt.pause(0.05)

plt.show()

print('Bye.')