from timeit import timeit

slow = """
import numpy as np
N = 5000

ex_array = np.zeros((N,), dtype='uint8')
for index in range(N):
    ex_array[index] = index % 37
"""
        
fast = """
import pymp
N = 5000

ex_array = pymp.shared.array((N,), dtype='uint8')
with pymp.Parallel(4) as p: 
    for index in p.range(N):
        ex_array[index] = index % 37
"""

print(f'slow: {timeit(slow, number=100)}')
print(f'fast: {timeit(slow, number=100)}')
