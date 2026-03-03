import numpy as np

def simple_iteraion_method(matrix: np.array, vector: np.array)-> float|int:
    tau = 2 / np.linalg.norm(matrix, np.inf)
    B = np.eye(len(matrix)) - tau * matrix
    g = tau * vector
    x_prev = g
    x_new = B @ x_prev + g
    iteration = 0
    while np.linalg.norm(x_prev-x_new, np.inf) > 10**(-5):
        x_prev = x_new
        x_new = B @ x_prev + g
        iteration+=1
    return x_new, iteration

system = np.array([
    [0.6137, -0.0808, 0.0162, 0.0323, 0.1131],
    [0.0840, 0.9609, 0.0000, -0.0646, 0.0646],
    [0.0485, 0.0000, 0.7720, -0.2261, 0.1292],
    [-0.0969, 0.2035, 0.0000, 0.7591, -0.0323],
    [0.4038, 0.0000, 0.1454, 0.0162, 0.9044]])

b = np.array([-3.4561, 2.9603, 2.8036, -2.0058, 2.3256])

x, iterations = simple_iteraion_method(system, b)

print(x)
print(iterations)
r = b - system @ x
print(r, '\n', np.linalg.norm(r, np.inf))