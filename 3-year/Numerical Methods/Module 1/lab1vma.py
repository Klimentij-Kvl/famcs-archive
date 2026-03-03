import numpy as np

def change_system_for_select_main_element(system, j):
    max_row = max(system[j:], key=lambda row: row[j])
    max_index = system.index(max_row)
    system[max_index], system[j] = system[j], system[max_index]
    m = 1 if max_index == 0 else -1
    return system, m

def straight_stroke(a):
    n = len(a)
    for k in range(0,n):
        a,m = change_system_for_select_main_element(a,k)
        for j in range(n,k-1,-1):
            a[k][j] /= a[k][k]
        for i in range(k+1,n):
            for j in range(n,k-1,-1):
                a[i][j] = a[i][j] - a[i][k]*a[k][j]
    return a

def reverse_stroke(a):
    n = len(a)
    x = [0] * n
    x[n-1] = a[n-1][n]
    for i in range(n-2,-1,-1):
        s = 0
        for j in range(i+1,n):
            s+=a[i][j]*x[j]
        x[i] = a[i][n] - s
    return x

def determinant(a):
    determinant = 1
    n = len(a)
    for k in range(0,n):
        a,m = change_system_for_select_main_element(a,k)
        determinant *= a[k][k] * m
        for j in range(n,k-1,-1):
            a[k][j] /= a[k][k]
        for i in range(k+1,n):
            for j in range(n,k-1,-1):
                a[i][j] = a[i][j] - a[i][k]*a[k][j]
    return determinant

def inverse_matrix(a):
    n = len(a)
    inverted_matrix = [[0] * n for _ in range(0,n)]
    for i in range(0,n):
        wired_matrix = [[0]*(n+1)]*n
        for j in range(0,n):
            wired_matrix[j] = [*a[j], 1 if j==i else 0]
        column = reverse_stroke(straight_stroke(wired_matrix))
        print(column)
        for j in range(0,n):
            inverted_matrix[j][i] = column[j]
    return inverted_matrix

system =  [
    [0.6137, -0.0808, 0.0162, 0.0323, 0.1131, -3.4561],
    [0.0840, 0.9609, 0.0000, -0.0646, 0.0646, 2.9603],
    [0.0485, 0.0000, 0.7720, -0.2261, 0.1292, 2.8036],
    [-0.0969, 0.2035, 0.0000, 0.7591, -0.0323, -2.0058],
    [0.4038, 0.0000, 0.1454, 0.0162, 0.9044, 2.3256]]
#print(system)

#print(determinant(system))
system2 = straight_stroke(system)
x = reverse_stroke(system2)
#for row in  system2:
#    print(row)
#print(x)

a = np.array([
    [0.6137, -0.0808, 0.0162, 0.0323, 0.1131],
    [0.0840, 0.9609, 0.0000, -0.0646, 0.0646],
    [0.0485, 0.0000, 0.7720, -0.2261, 0.1292],
    [-0.0969, 0.2035, 0.0000, 0.7591, -0.0323],
    [0.4038, 0.0000, 0.1454, 0.0162, 0.9044]])
b = np.array([-3.4561, 2.9603, 2.8036, -2.0058, 2.3256])
y = np.array(x)
z = a @ y - b
#print(np.linalg.norm(z,ord=1))

system3 = [
    [0.6137, -0.0808, 0.0162, 0.0323, 0.1131],
    [0.0840, 0.9609, 0.0000, -0.0646, 0.0646],
    [0.0485, 0.0000, 0.7720, -0.2261, 0.1292],
    [-0.0969, 0.2035, 0.0000, 0.7591, -0.0323],
    [0.4038, 0.0000, 0.1454, 0.0162, 0.9044]]

b = np.array(inverse_matrix(system3))
z = a @ b - np.eye(5)
print(b)
print(z)
print(np.linalg.norm(a,ord=1) * np.linalg.norm(np.linalg.inv(a),ord=1))