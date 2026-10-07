import numpy as np

def get_c_matrix(matrix: np.ndarray)->np.ndarray:
    n = matrix.shape[0]
    c = np.zeros(shape=(5,6))
    c[0,0] = 1
    for i in range(1, n+1):
        c[:, i] = matrix @ c[:, i-1]
    return c

def get_q_matrix(c_matrix: np.ndarray)->np.ndarray:
    return np.linalg.solve(c_matrix[:, -2::-1], c_matrix[:, -1])

def get_beta_matrix(q_matrix: np.ndarray, eigvals: np.ndarray)->np.ndarray:
    n = q_matrix.shape[0]
    beta = np.zeros((n, n))
    for j in range(n):
        beta[0,j] = 1
        for i in range(1,n):
            beta[i,j] = eigvals[j] * beta[i-1,j] - q_matrix[i-1]
    return beta

def get_eigvecs(beta: np.ndarray, c_matrix: np.ndarray):
    n = beta.shape[0]
    x = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            x[:,i] += beta[j,i] * c_matrix[:,n-j-1]

    return x

def krylov_method(matrix: np.ndarray, eigvals: np.ndarray):
    c  =  get_c_matrix(matrix)
    q = get_q_matrix(c)
    beta = get_beta_matrix(q, eigvals)
    eigvecs = get_eigvecs(beta, c)
    return eigvecs

matrix = np.array([
    [0.55847999, 0.01140949, 0.10609646, -0.06358497, 0.44942866],
    [0.01140949, 0.9712697, -0.00130896, 0.08979287, 0.04636261],
    [0.10609646, -0.00130896, 0.6173876, -0.17167046, 0.23307438],
    [-0.06358497, 0.08979287, -0.17167046, 0.63283291, -0.0395998],
    [0.44942866, 0.04636261, 0.23307438, -0.03959984, 0.85264006]
])

eigvals = np.array([0.21706397778568032,
                    0.9996183063478336,
                    0.43586239368675883,
                    0.6792087361485457, 
                    1.3008568460311822])


matrix2 = np.array([[0.37027355, 0.00756217, 0.07035566, -0.04215561, 0.29797900],
                    [0.00756217, 0.64393589, -0.00086856, 0.05953439, 0.03073615],
                    [0.07035566, -0.00086856, 0.40933076, -0.11381522, 0.15453420],
                    [-0.04215561, 0.05953439, -0.11381522, 0.41957311, -0.02624740],
                    [0.29797900, 0.03073615, 0.15453420, -0.02624740, 0.56529286]])

eigvals2 = np.array([0.1439066147000975,
0.6627338021549952,
0.2889769977818668,
0.4503145434825520,
0.8624742118804892])

c = get_c_matrix(matrix)
print('c:')
for st in c:
    for elem in st:
        print(np.round(elem,9), end=' & ')
    print('\\\\')
q = get_q_matrix(c)
for st in q:
    print(np.round(st,9), end=' & ')
print('q:')
print(q)
beta = get_beta_matrix(q, eigvals)
print('beta:')
for st in beta:
    for elem in st:
        print(np.round(elem,9), end=' & ')
    print('\\\\')
x = get_eigvecs(beta, c)
print('x:')
for st in x:
    for elem in st:
        print(np.round(elem,9), end=' & ')
    print('\\\\')

print(matrix @ x[:,0] - eigvals[0] * x[:,0])

# coeffs = np.ones(q.shape[0]+1)
# coeffs[1:] = q
# print(np.roots(coeffs))

eigv, eigvecs = np.linalg.eig(matrix2)
#print(eigv)
# print(eigvecs)
for i  in range(5):
    print(matrix @ x[:,i] - eigvals[i] * x[:,i])