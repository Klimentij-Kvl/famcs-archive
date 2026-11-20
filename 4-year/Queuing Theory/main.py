import numpy as np
import math

def calculate_bmap_matrices(D_dict, theta_tilde, N_max, J_max, t, beta, S):
    """
    Выполняет расчет матриц K, P, Y для системы BMAP/G/1.
    """
    
    # Приводим beta к одномерному массиву (на всякий случай)
    beta = np.array(beta).flatten() 
    
    # Определяем размерность матриц (W+1)
    W = D_dict[0].shape[0]
    I = np.eye(W)
    O = np.zeros((W, W))
    
    def get_D(k):
        return D_dict.get(k, np.zeros((W, W)))

    # =========================================================================
    # ШАГ 1. Расчет матриц K_n^(j) по формуле (3.8)
    # =========================================================================
    K = np.zeros((J_max + 1, N_max + 1, W, W))
    
    K[0][0] = I.copy()
    for n in range(1, N_max + 1):
        K[0][n] = O.copy()
        
    inv_theta = 1.0 / theta_tilde
    D0 = get_D(0)
    I_plus_D0 = I + inv_theta * D0
    
    for j in range(J_max):
        K[j+1][0] = K[j][0] @ I_plus_D0
        for n in range(1, N_max + 1):
            sum_term = np.zeros((W, W))
            for i in range(n):
                sum_term += K[j][i] @ get_D(n - i)
            K[j+1][n] = inv_theta * sum_term + K[j][n] @ I_plus_D0

    # =========================================================================
    # ШАГ 2. Расчет матриц P(n, t) по формуле (3.7)
    # =========================================================================
    P = np.zeros((N_max + 1, W, W))
    exp_factor = math.exp(-theta_tilde * t)
    
    for n in range(N_max + 1):
        for j in range(J_max + 1):
            weight = exp_factor * ((theta_tilde * t) ** j) / math.factorial(j)
            P[n] += weight * K[j][n]

    # =========================================================================
    # ШАГ 3 и 4. Расчет гамма_j и матриц Y_l
    # =========================================================================
    m = S.shape[0] 
    S0 = -S @ np.ones(m) 
    M_matrix = theta_tilde * np.eye(m) - S 
    M_inv = np.linalg.inv(M_matrix)
    
    gamma = np.zeros(J_max + 1)
    
    # ИСПРАВЛЕНИЕ: Используем .item() для извлечения скаляра
    current_M_power = M_inv.copy()
    gamma[0] = (beta @ current_M_power @ S0).item() 
    
    for j in range(1, J_max + 1):
        current_M_power = current_M_power @ M_inv
        # ИСПРАВЛЕНИЕ: Используем .item() для извлечения скаляра
        gamma[j] = ((theta_tilde ** j) * (beta @ current_M_power @ S0)).item()

    # Расчет матриц Y_l
    Y = np.zeros((N_max + 1, W, W))
    for l in range(N_max + 1):
        for j in range(J_max + 1):
            Y[l] += gamma[j] * K[j][l]

    return K, P, Y, gamma


# =========================================================================
# ПРИМЕР ИСПОЛЬЗОВАНИЯ
# =========================================================================
if __name__ == "__main__":
    D0 = np.array([[-2.0,  0.5],
                   [ 0.2, -1.5]])
    D1 = np.array([[ 1.0,  0.5],
                   [ 0.8,  0.5]])
    D_dict = {0: D0, 1: D1} 
    
    theta_tilde = max([-D0[i, i] for i in range(D0.shape[0])]) 
    
    N_max = 3      
    J_max = 100     
    t = 1.0         
    
    # Можете передавать beta как [[1.0]] или как [1.0] — код теперь справится
    beta = np.array([1.0]) 
    S = np.array([[-1.5]])
    
    K_matrices, P_matrices, Y_matrices, gammas = calculate_bmap_matrices(
        D_dict, theta_tilde, N_max, J_max, t, beta, S
    )
    
    print("--- Коэффициенты гамма (первые 5) ---")
    print(gammas[:5])
    
    print("\n--- Матрица P(0, t) ---")
    print(np.round(P_matrices[0], 4))
    
    print("\n--- Матрица P(1, t) ---")
    print(np.round(P_matrices[1], 4))
    
    print("\n--- Матрица Y_0 (вложенная цепь Маркова) ---")
    print(np.round(Y_matrices[0], 4))