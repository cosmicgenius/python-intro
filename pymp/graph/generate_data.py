import numpy as np
N = 1024

with open("data.txt", "w") as f:
    labels = [hex(i + 1) for i in range(N)]
    np.random.shuffle(labels)
    for i in range(N):
        f.write(f'{i} {labels[i]}\n')
    
    graph_weights = np.random.rand(N, N)

    for i in range(N):
        f.write("\n")
        f.write(f'{i}\n')
        for j in range(N):
            if i == j or graph_weights[i][j] < 0.3:
                continue
            f.write(f'{j} {graph_weights[i][j]}\n')



