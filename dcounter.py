from collections import deque
import pickle

edgelist = []
current = 1
for i in range(1, 10):
    for j in range(1, 13):
        if i == 1:
            if j == 1:
                edgelist.append((current, current + 1))
                edgelist.append((current, current + 12))
            elif j == 12:
                edgelist.append((current, current - 1))
                edgelist.append((current, current + 12))
                edgelist.append((current, current + 11))
            else:
                if current % 2 == 0:
                    edgelist.append((current, current + 11))
                    edgelist.append((current, current + 13))
                edgelist.append((current, current - 1))
                edgelist.append((current, current + 1))
                edgelist.append((current, current + 12))
        elif i == 9:
            if j == 1:
                edgelist.append((current, current + 1))
                edgelist.append((current, current - 12))
                edgelist.append((current, current - 11))
            elif j == 12:
                edgelist.append((current, current - 1))
                edgelist.append((current, current - 12))
            else:
                if current % 2 == 1:
                    edgelist.append((current, current - 11))
                    edgelist.append((current, current - 13))
                edgelist.append((current, current - 1))
                edgelist.append((current, current + 1))
                edgelist.append((current, current - 12))
        elif j == 1:
            edgelist.append((current, current - 11))
            edgelist.append((current, current - 12))
            edgelist.append((current, current + 12))
            edgelist.append((current, current + 1))
        elif j == 12:
            edgelist.append((current, current + 11))
            edgelist.append((current, current - 12))
            edgelist.append((current, current + 12))
            edgelist.append((current, current - 1))
        else:
            if current % 2 == 0:
                edgelist.append((current, current + 11))
                edgelist.append((current, current + 13))
            else:
                edgelist.append((current, current - 11))
                edgelist.append((current, current - 13))
            edgelist.append((current, current - 1))
            edgelist.append((current, current + 1))
            edgelist.append((current, current - 12))
            edgelist.append((current, current + 12))

        current += 1
adj_list = {key: [] for key in range(1, 109)}
print(set(edgelist))
for edge in set(edgelist):
    if edge[1] not in adj_list[edge[0]]:
        adj_list[edge[0]].append(edge[1])
    if edge[0] not in adj_list[edge[1]]:
        adj_list[edge[1]].append(edge[0])

print(adj_list)
dist_records = {key: {} for key in range(1, 109)}

def BFS(source):
    Q = deque()
    Q.append(source)

    visited = set()
    visited.add(source)
    dist_records[source][source] = 0
    count = 1
    while Q:
        v = Q.popleft()
        for neighbour in adj_list[v]:
            if neighbour not in visited:
                Q.append(neighbour)
                visited.add(neighbour)
                dist_records[source][neighbour] = dist_records[source][v] + 1
        count += 1

for i in range(1, 109):
    BFS(i)

print(dist_records[25][70])

def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

save_obj(dist_records, "distances")

