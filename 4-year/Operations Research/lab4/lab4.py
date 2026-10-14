N = int(input())
N += 1

prices = list(map(int, input().split()))
weights = list(map(int, input().split()))

W = int(input())
W += 1

matrix = [[0] * N for _ in range(W)]

for i in range(W):
    for j in range(1, N):
        if i < weights[j - 1]:
            matrix[i][j] = matrix[i][j - 1]
        else:
            last = matrix[i][j - 1]
            nxt = matrix[i - weights[j - 1]][j] + prices[j - 1]
            matrix[i][j] = max(last, nxt)

i = W - 1
j = N - 1
counts = [0] * (N - 1)

while i > 0 and j > 0:
    if matrix[i][j] == matrix[i][j - 1]:
        j -= 1
    else:
        counts[j - 1] += 1
        i -= weights[j - 1]

print("Количество каждого предмета:", counts)
print("Максимальная стоимость:", matrix[W - 1][N - 1])