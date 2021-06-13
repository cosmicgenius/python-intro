import pymp
from timeit import timeit

N = 10000000

def slow():
    a = [0] * N
    for i in range(N):
        a[i] = 1

def fast():
    a = pymp.shared.array((N,))
    b = a
    c = a
    d = a
    e = a
    with pymp.Parallel(4) as p:
        num_per = N // p.num_threads
        if p.thread_num == 0:
            f = b
        elif p.thread_num == 1:
            f = c
        elif p.thread_num == 2:
            f = d
        elif p.thread_num == 3:
            f = e
        for index in range(num_per * p.thread_num, num_per * (p.thread_num + 1)):
            f[index] = 1

def fast2():
    a = pymp.shared.array((N,))
    with pymp.Parallel(4) as p:
        for i in p.range(N):
            a[i] = 1

print(timeit(lambda: slow(), number=1))
print(timeit(lambda: fast(), number=1))
print(timeit(lambda: fast2(), number=1))
