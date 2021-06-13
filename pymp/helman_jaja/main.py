# Task:
# Generate indices of a linked list given successors
# Implementation: https://downey.io/blog/helman-jaja-list-ranking-explained/

from timeit import timeit
import pymp
import numpy as np

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
    heads = 40

    sublist_head = list(np.random.choice(range(N), heads, replace=False))
    if not head in sublist_head:
        sublist_head.append(head)


    head_to_sublist = { head: sl_idx for sl_idx, head in enumerate(sublist_head) }

    sublists = len(sublist_head)
        
    partial_ranking = pymp.shared.array((N,), dtype=int)
    parent_sublist = pymp.shared.list([None] * N)
    stop = [None] * N

    sublist_length = pymp.shared.array((sublists,), dtype=int)
    sublist_succ = pymp.shared.array((sublists,), dtype=int)
    
    ranking = pymp.shared.array((N,), dtype=int)

    for head in sublist_head:
        stop[head] = True

    print(0)
    with pymp.Parallel(4) as p:
        for sl_idx in p.range(sublists):
            current_idx = sublist_head[sl_idx]
            rank = 0

            while current_idx != -1 and (current_idx == sublist_head[sl_idx] or not stop[current_idx]):
                partial_ranking[current_idx] = rank
                parent_sublist[current_idx] = sl_idx

                rank += 1
                current_idx = successor[current_idx]
                
            sublist_length[sl_idx] = rank
            if current_idx == -1:
                sublist_succ[sl_idx] = -1
            else:
                sublist_succ[sl_idx] = head_to_sublist[current_idx]

    # shared variables
    # 1. do not work in different mp instances
    # and 2. are far slower than normal ones
    # so we convert them here
    sublist_offset_abs = [0] * sublists
    parent_sublist = list(parent_sublist)
    partial_ranking = list(partial_ranking)

    current_sl = head_to_sublist[head]
    while sublist_succ[current_sl] != -1:
        sublist_offset_abs[sublist_succ[current_sl]] = sublist_offset_abs[current_sl] + sublist_length[current_sl]
        current_sl = sublist_succ[current_sl]

    print(1)
    with pymp.Parallel(4) as p:
        for i in p.range(N):
            ranking[i] = sublist_offset_abs[parent_sublist[i]] + partial_ranking[i]
    print(2)

    return list(ranking)
        

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

    print("Slow (single processor):", timeit(lambda: answers.append(slow(head, successor)), setup='from __main__ import answers', number=1))
    print("Fast (4 processors):", timeit(lambda: answers.append(fast(head, successor)), setup='from __main__ import answers', number=1))

    ans_slow = answers[0]
    ans_fast = answers[1]

    works = (list(ans_slow) == list(ans_fast))

    print("Correct values?:", "yes" if works else "no")
    # if not works:
    #     print(ans_slow)
    #     print(ans_fast)

