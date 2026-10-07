import numpy as np

def find_M(n: int, A: np.ndarray)->np.ndarray:
    m = len(A)
    n-=1
    M = np.eye(m)
    for i in range(m):
        M[n-1][i] = -A[n][i]/A[n][n-1] if i != (n-1) else 1/A[n][n-1]
    return M

def find_P_coef(A: np.ndarray)->np.ndarray:
    m = len(A)
    B = A
    for i in range(m-1):
        M = find_M(m-i, B)
        B = np.linalg.inv(M) @ B @ M
    return B[0]

def find_root_char(coeffs: np.ndarray, eigval: float):
    n = len(coeffs)
    coeffs2 = [-1] + coeffs.tolist()
    root = 0
    for i in range(n+1):
        root -= coeffs2[i] * eigval ** (n-i)
    return root * (-1)**n

matrix = np.array([
    [0.55847999, 0.01140949, 0.10609646, -0.06358497, 0.44942866],
    [0.01140949, 0.9712697, -0.00130896, 0.08979287, 0.04636261],
    [0.10609646, -0.00130896, 0.6173876, -0.17167046, 0.23307438],
    [-0.06358497, 0.08979287, -0.17167046, 0.63283291, -0.0395998],
    [0.44942866, 0.04636261, 0.23307438, -0.03959984, 0.85264006]
])
#for i in range(5):
#    print(find_M(i+1,matrix),'\n')
#print(np.linalg.inv(find_M(4,matrix)))

coef = find_P_coef(matrix)
print(coef)
eigvals = np.array([0.21706397778568032,
                    0.9996183063478336,
                    0.43586239368675883,
                    0.6792087361485457, 
                    1.3008568460311822])
n = len(coef)
for j in range(n):
    print(find_root_char(coef, eigvals[j]))

exp = [1] + (-coef).tolist()
print(np.roots(exp))

#eigenvalues, eigenvectors = np.linalg.eig(matrix)

#print("Собственные значения:")
#print(eigenvalues)
