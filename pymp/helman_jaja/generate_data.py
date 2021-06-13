import numpy as np
N = 262144

arr = np.arange(N)
np.random.shuffle(arr)

with open('data.txt', 'w') as f:
    successor = [-1 for i in range(N)]

    for i in range(N - 1):
        successor[arr[i]] = arr[i + 1]

    for s in successor:
        f.write(f'{s}\n')

