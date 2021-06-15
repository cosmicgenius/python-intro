# Task:
# Generate indices of a linked list given successors
# Implementation: https://downey.io/blog/helman-jaja-list-ranking-explained/

from timeit import timeit
from datetime import datetime
import pymp
import numpy as np

def fast_choice(N, M):
    res = set()

    while len(res) < M:
        for r in np.random.rand(M):
            res.add(int(r * N))

    return list(res)

def slow(head, successor):
    # Process data
    N = len(successor)
    ranking = [0] * N
    current_idx = head
    
    for i in range(1, N):
        current_idx = successor[current_idx]
        ranking[current_idx] = i

    return ranking

def fast(head, successor):
    # Process data
    N = len(successor)
    heads = 400

    sublist_head = fast_choice(N, heads)
    if not head in sublist_head:
        sublist_head.append(head)


    head_to_sublist = { head: sl_idx for sl_idx, head in enumerate(sublist_head) }

    sublists = len(sublist_head)
        
    print(0, datetime.now().time())

    parent_sublist = pymp.shared.array((N,), dtype=int) # sublist index + 1
    stop = { -1: True }

    sublist_length = pymp.shared.array((sublists,), dtype=int)
    sublist_succ = pymp.shared.array((sublists,), dtype=int)
    
    ranking = pymp.shared.array((N,), dtype=int)

    for sl_idx, head in enumerate(sublist_head):
        stop[head] = True
        parent_sublist[head] = sl_idx

    print(1, datetime.now().time())
    with pymp.Parallel(4) as p:
        for sl_idx in p.range(sublists):
            current_idx = successor[sublist_head[sl_idx]]

            for rank in range(1, N):
                if stop.get(current_idx) != None:
                    sublist_length[sl_idx] = rank
                    break

                ranking[current_idx] = rank
                parent_sublist[current_idx] = sl_idx

                current_idx = successor[current_idx]

            sublist_succ[sl_idx] = -1 if current_idx == -1 else head_to_sublist.get(current_idx) 
    
    print(2, datetime.now().time())

    # shared variables
    # 1. do not work in different mp instances
    # and 2. are far slower than normal ones
    # so we convert them here
    sublist_offset_abs = [0] * sublists

    current_sl = head_to_sublist[head]
    while sublist_succ[current_sl] != -1:
        sublist_offset_abs[sublist_succ[current_sl]] = sublist_offset_abs[current_sl] + sublist_length[current_sl]
        current_sl = sublist_succ[current_sl]

    print(3, datetime.now().time())

    with pymp.Parallel(4) as p:
        for i in p.range(N):
            ranking[i] += sublist_offset_abs[parent_sublist[i]]

    print(4, datetime.now().time())

    return ranking
        

with open('data.txt') as f:
    # Read data
    line = f.readline()
    successor = []
    total = 0

    while line:
        idx = int(line)
        total += idx

        successor.append(idx)
        line = f.readline()

    # the successor list will contain 0 to len(successor) - 1
    # but with the head replaced with -1
    # hence head = total without the replaced - total with replaced - 1
    head = len(successor) * (len(successor) - 1) // 2 - total - 1
    
    answers = []

    print('start')
    
    t_fast = timeit(lambda: answers.append(fast(head, successor)), setup='from __main__ import answers', number=1)
    print("Fast (4 processors):", t_fast)

    t_slow = timeit(lambda: answers.append(slow(head, successor)), setup='from __main__ import answers', number=1)
    print("Slow (single processor):", t_slow)
    
    print("Fast was", "faster" if t_fast < t_slow else "slower", "than slow by:", f"{np.sign(t_fast - t_slow) * (t_fast / t_slow - 1) * 100}%")

    ans_slow = answers[0]
    ans_fast = answers[1]

    works = (list(ans_slow) == list(ans_fast))

    print("Correct values?:", "yes" if works else "no")
    # if not works:
    #     print(ans_slow)
    #     print(ans_fast)
    
