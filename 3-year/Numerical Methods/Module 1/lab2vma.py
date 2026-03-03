import numpy as np
import math

def cholesky_decomposition(matrix):
    n = len(matrix)
    cholesky_matrix = [[0.0] * n for _ in range(n)]
    cholesky_matrix[0][0] = math.sqrt(matrix[0][0])

    for j in range(1,n):
        cholesky_matrix[0][j] = matrix[0][j] / cholesky_matrix[0][0]

    for i in range(1,n):
        sq_sum = sum(cholesky_matrix[k][i] ** 2 for k in range(i))
        cholesky_matrix[i][i] = math.sqrt(matrix[i][i] - sq_sum)
        for j in range(i+1,n):
            summ = sum(cholesky_matrix[k][i] * cholesky_matrix[k][j] for k in range(i))
            cholesky_matrix[i][j] = (matrix[i][j] - summ) / cholesky_matrix[i][i]

    return cholesky_matrix

def first_equattion(b, s):
    n = len(b)
    y = [0.0] * n
    y[0] = b[0] / s[0][0]
    for i in range(1,n):
        summ = 0
        for j in range(0,i):
            summ += s[j][i] * y[j]
        y[i] = (b[i] - summ) / s[i][i]
    return y

def second_equation(y,s):
    n =  len(y)
    x = [0.0] * n
    x[n-1] = y[n-1] * s[n-1][n-1]
    for i in range(n-1,-1,-1):
        summ = 0
        for j in range(i+1,n):
            summ+= s[i][j] * x[j]
        x[i] = (y[i] - summ) / s[i][i]
    return x

def square_root_method(matrix, b):
    s = cholesky_decomposition(matrix)
    y = first_equattion(b,s)
    return second_equation(y,s)

matrix = [
    [0.55847999, 0.01140949, 0.10609646, -0.06358497, 0.44942866],
    [0.01140949, 0.9712697, -0.00130896, 0.08979287, 0.04636261],
    [0.10609646, -0.00130896, 0.6173876, -0.17167046, 0.23307438],
    [-0.06358497, 0.08979287, -0.17167046, 0.63283291, -0.0395998],
    [0.44942866, 0.04636261, 0.23307438, -0.03959984, 0.85264006]
]

b = [-0.60292947, 2.71562485, 2.44653262, -2.42168943, 2.33063557]

"""
for row in cholesky_decomposition(matrix):
    print(row)

print(first_equattion(b, cholesky_decomposition(matrix)))
"""

s = cholesky_decomposition(matrix)
y = first_equattion(b,s)
"""
for row in s:
    for elem in row:
        print(round(elem, 11), end="& ")
    print("\\\\",  end = "\n")
"""
#print(y)
#print(s)
#print(y)
x = square_root_method(matrix,b)
print(x)
print( np.array(matrix) @ np.array(x) - np.array(b) )

a_1 = np.array([
    [0.6137, -0.0808, 0.0162, 0.0323, 0.1131],
    [0.0840, 0.9609, 0.0000, -0.0646, 0.0646],
    [0.0485, 0.0000, 0.7720, -0.2261, 0.1292],
    [-0.0969, 0.2035, 0.0000, 0.7591, -0.0323],
    [0.4038, 0.0000, 0.1454, 0.0162, 0.9044]])
b_1 = np.array([-3.4561, 2.9603, 2.8036, -2.0058, 2.3256])
y = np.array(x)
z = a_1 @ y - b_1
print(z)