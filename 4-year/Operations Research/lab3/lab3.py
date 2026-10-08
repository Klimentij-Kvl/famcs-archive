
import heapq

N, M = map(int, input().split())

graph = [[] for _ in range(N + 1)]
degree = [0] * (N + 1)

for _ in range(M):
    u, v, w = map(int, input().split())

    graph[u].append((v, w))
    graph[v].append((u, w))

    degree[u] += 1
    degree[v] += 1

s, f, q = map(int, input().split())

INF = 10**30

dist = [INF] * (N + 1)
dist[s] = 0

heap = [(0, s)]

while heap:
    cur_dist, u = heapq.heappop(heap)

    if cur_dist != dist[u]:
        continue
    if u == f:
        break

    for v, road_time in graph[u]:
        new_dist = cur_dist + road_time + q * degree[u]

        if new_dist < dist[v]:
            dist[v] = new_dist
            heapq.heappush(heap, (new_dist, v))

if dist[f] == INF:
    print("No")
else:
    print("Yes")
    print(dist[f])