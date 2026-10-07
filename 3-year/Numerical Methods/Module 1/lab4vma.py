import numpy as np
#->tuple[np.ndarray, int]

def cdm_iteration(x_prev: np.ndarray, a: np.ndarray, b: np.ndarray)->np.ndarray:
    n = len(x_prev)
    x_new = np.array([0.] * n)
    for i in range(0,n):
        x_new[i]=0
        for j in range(0,i):
            x_new[i] -= a[i][j] / a[i][i] * x_new[j]
        for j in range(i+1,n):
            x_new[i] -= a[i][j] / a[i][i] * x_prev[j]
        x_new[i] += b[i]/a[i][i]
    return x_new

def coordinate_descent_method(a: np.ndarray, b: np.ndarray)->tuple[np.ndarray, int]:
    x_prev = b
    x_new = cdm_iteration(x_prev, a, b)
    iteration = 0
    while np.linalg.norm(x_prev - x_new, np.inf) > 10**(-5):
        iteration+=1
        x_prev = x_new
        x_new = cdm_iteration(x_prev, a, b)
        
    return x_new, iteration

matrix = np.array([
    [0.55847999, 0.01140949, 0.10609646, -0.06358497, 0.44942866],
    [0.01140949, 0.9712697, -0.00130896, 0.08979287, 0.04636261],
    [0.10609646, -0.00130896, 0.6173876, -0.17167046, 0.23307438],
    [-0.06358497, 0.08979287, -0.17167046, 0.63283291, -0.0395998],
    [0.44942866, 0.04636261, 0.23307438, -0.03959984, 0.85264006]
])

b = np.array(
    [-0.60292947, 2.71562485, 2.44653262, -2.42168943, 2.33063557]
)

x, iter = coordinate_descent_method(matrix, b)

for elem in x:
    print(elem, "\\\\", end=' ')



print()
print(x)
print('Количество итераций: ', iter)

R = np.array(b - matrix @ x)

for elem in R:
    print(elem, "\\\\", end=' ')

print()
print(np.linalg.norm(R, ord=np.inf))