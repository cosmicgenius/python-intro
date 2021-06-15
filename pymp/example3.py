from timeit import timeit

p = 1299709

def slow():
    a = 2
    b = 1

    while a % p != 1:
        a = a * 2 % p
        b += 1

    return b

def fast():
    a = 2
    for b in range(1, p):
        if a % p == 1:
            return b
        a = a * 2 % p
    return 'what' 

print(timeit(lambda: slow(), number=50))
print(timeit(lambda: fast(), number=50))
