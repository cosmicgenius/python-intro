from timeit import timeit
import numpy as np

N = 10000000
M = 40

arr = np.arange(N)
np.random.shuffle(arr)

def np_choice():
    return np.random.choice(arr, M, replace=False)

def my_choice():
    res = set()

    while len(res) < M:
        for r in np.random.rand(M):
            res.add(arr[int(r * N)])

    return list(res)

print(timeit(lambda: np_choice(), number=1))
print(timeit(lambda: my_choice(), number=1))

