"""dcounter.py: Finds and saves distances between every set of spaces on a Cryptid map. The map is represented with
each space as a vertex in graph with edges to all neighboring spaces. Then BFS is run to find all the correct
distances. Distances saved as a dictionary in distances.pkl"""
__author__ = "Christopher Lehman"
__email__ = "lehman40@purdue.edu"

from collections import deque
import pickle

edgelist = []
current = 1
for i in range(1, 10):  # Loop through all 9 rows
    for j in range(1, 13):  # Loop through all 12 columns
        if i == 1:
            if j == 1:  # Top left corner
                edgelist.append((current, current + 1))
                edgelist.append((current, current + 12))
            elif j == 12:  # Top right corner
                edgelist.append((current, current - 1))
                edgelist.append((current, current + 12))
                edgelist.append((current, current + 11))
            else:  # Top row
                if current % 2 == 0:  # Even numbered indices have more edges
                    edgelist.append((current, current + 11))
                    edgelist.append((current, current + 13))
                edgelist.append((current, current - 1))
                edgelist.append((current, current + 1))
                edgelist.append((current, current + 12))
        elif i == 9:
            if j == 1:  # Bottom left corner
                edgelist.append((current, current + 1))
                edgelist.append((current, current - 12))
                edgelist.append((current, current - 11))
            elif j == 12:  # Bottom right corner
                edgelist.append((current, current - 1))
                edgelist.append((current, current - 12))
            else:  # Bottom row
                if current % 2 == 1:  # Odd numbered indices have more edges
                    edgelist.append((current, current - 11))
                    edgelist.append((current, current - 13))
                edgelist.append((current, current - 1))
                edgelist.append((current, current + 1))
                edgelist.append((current, current - 12))
        elif j == 1:  # Left column
            edgelist.append((current, current - 11))
            edgelist.append((current, current - 12))
            edgelist.append((current, current + 12))
            edgelist.append((current, current + 1))
        elif j == 12:  # right column
            edgelist.append((current, current + 11))
            edgelist.append((current, current - 12))
            edgelist.append((current, current + 12))
            edgelist.append((current, current - 1))
        else:  # Any space in the middle, always has six neighbors
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
# print(set(edgelist))

for edge in set(edgelist):  # add all edges to the adjacency list representation
    if edge[1] not in adj_list[edge[0]]:
        adj_list[edge[0]].append(edge[1])
    if edge[0] not in adj_list[edge[1]]:
        adj_list[edge[1]].append(edge[0])

# print(adj_list)
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

# check distances
# print(dist_records[25][70])

# save results to file
def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

save_obj(dist_records, "distances")

