# Task:
# Given a directed graph, for each vertex u, find the sum
# of the weights of v -> w for all v, w such that 
# u -> v -> w (with some names for each vertex included)
#
# Objective:
# Test how to use pymp on stuff like this.

import math
from timeit import timeit
import pymp

def slow():
    with open("data.txt") as f:
        # Read from the file
        line = f.readline()

        name_map = {}

        while line != "\n":
            u, name = line[0:-1].split()
            name_map[u] = name

            line = f.readline()

        adj_list = { u: {} for u in name_map.keys() }
        
        while line:
            line = f.readline()
            u = line[0:-1]

            line = f.readline()
            while line and line != "\n":
                v, weight = line[0:-1].split()
                adj_list[u][v] = float(weight)
                line = f.readline()
        
        # Process data
        answer = {}
        for u in name_map.keys():
            total = 0
            for v in adj_list[u].keys():
                for weight in adj_list[v].values():
                    total += weight

            answer[name_map[u]] = total

        return { name: ans for name, ans  in sorted(answer.items(), key = lambda o: o[0]) }

def fast():
    with open("data.txt") as f:
        # Read from the file
        line = f.readline()

        proto_name_map = {}

        while line != "\n":
            u, name = line[0:-1].split()
            proto_name_map[u] = name

            line = f.readline()

        proto_adj_list = { u: {}  for u in proto_name_map.keys() }
        
        while line:
            line = f.readline()
            u = line[0:-1]
            
            line = f.readline()
            while line and line != "\n":
                v, weight = line[0:-1].split()
                proto_adj_list[u][v] = float(weight)
                line = f.readline()

        name_map = pymp.shared.dict(proto_name_map)
        adj_list = proto_adj_list
        
        # Process data
        answer = pymp.shared.dict()
        with pymp.Parallel(4) as p:
            vertices = name_map.keys()
            for idx in p.range(len(vertices)):
                u = vertices[idx]

                total = 0
                for v in adj_list[u].keys():
                    for weight in adj_list[v].values():
                        total += weight

                answer[name_map[u]] = total

        return { name: ans for name, ans  in sorted(answer.items(), key = lambda o: o[0]) }

answers = []

print("Slow (single processor):", timeit(lambda: answers.append(slow()), setup='from __main__ import answers', number=1))
print("Fast (4 processors):", timeit(lambda: answers.append(fast()), setup='from __main__ import answers', number=1))

ans_slow = answers[0]
ans_fast = answers[1]

works = True
for name in ans_slow.keys():
    if not name in ans_fast or not math.isclose(ans_slow[name], ans_fast[name]):
        works = False
        break

print("Correct values?:", "yes" if works else "no")
