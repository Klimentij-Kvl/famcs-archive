import numpy as np
import math
from scipy.optimize import linprog
from collections import defaultdict, deque

# ==========================================
# ИСХОДНЫЕ ДАННЫЕ (Вариант 16)
# ==========================================
# Формат: 'работа': (предшественники, t_пес, t_вер, t_опт, стоимость_сокращения)
tasks = {
    'b1': ([], 15, 11, 3, 9),
    'b2': ([], 14, 10, 2, 5),
    'b3': ([], 11, 9, 4, 7),
    'b4': (['b1'], 16, 13, 6, 3),
    'b5': (['b2'], 9, 7, 2, 5),
    'b6': (['b2'], 7, 5, 3, 10),
    'b7': (['b3', 'b6'], 8, 5, 1, 9),
    'b8': (['b7'], 9, 6, 1, 7),
    'b9': (['b7'], 12, 8, 4, 6),
    'b10': (['b4', 'b5', 'b8'], 11, 6, 3, 11),
    'b11': (['b9', 'b10'], 13, 10, 7, 14),
    'b12': (['b3', 'b5'], 16, 14, 8, 8)
}

T_dir = 40
gamma = 0.95
S = 14 # Стоимость одного дня проекта

# Построение сетевого графа (Activity-on-Node -> Activity-on-Arc)
# Для удобства расчетов создадим фиктивные узлы
edges = []
durations_max = {}
durations_opt = {}
costs = {}

# Базовые узлы
# b1: 0->1, b2: 0->2, b3: 0->3
# b4: 1->4, b5: 2->5, b6: 2->6
# b7 зависит от b3, b6. Добавим узел 7. b3(0->3), b6(2->6). Фиктивные: 3->7, 6->7. b7: 7->8
# b8: 8->9, b9: 8->10
# b10 зависит от b4, b5, b8. Узел 11. Фиктивные: 4->11, 5->11, 9->11. b10: 11->12
# b11 зависит от b9, b10. Узел 13. Фиктивные: 10->13, 12->13. b11: 13->14
# b12 зависит от b3, b5. Узел 15. Фиктивные: 3->15, 5->15. b12: 15->16
# Конец: узел 17. Фиктивные: 14->17, 16->17

# Заполняем граф
node_map = {
    'b1': (0, 1), 'b2': (0, 2), 'b3': (0, 3),
    'b4': (1, 4), 'b5': (2, 5), 'b6': (2, 6),
    'b7': (7, 8), 'b8': (8, 9), 'b9': (8, 10),
    'b10': (11, 12), 'b11': (13, 14), 'b12': (15, 16)
}

# Добавляем реальные дуги
for t_name, (u, v) in node_map.items():
    edges.append((u, v, t_name))
    durations_max[t_name] = tasks[t_name][1]
    durations_opt[t_name] = tasks[t_name][3]
    costs[t_name] = tasks[t_name][4]

# Добавляем фиктивные дуги (длительность 0)
dummy_edges = [
    (3, 7, 'd1'), (6, 7, 'd2'),       # Для b7
    (4, 11, 'd3'), (5, 11, 'd4'), (9, 11, 'd5'), # Для b10
    (10, 13, 'd6'), (12, 13, 'd7'),   # Для b11
    (3, 15, 'd8'), (5, 15, 'd9'),     # Для b12
    (14, 17, 'd10'), (16, 17, 'd11')  # Конец проекта
]
for u, v, t_name in dummy_edges:
    edges.append((u, v, t_name))
    durations_max[t_name] = 0
    durations_opt[t_name] = 0
    costs[t_name] = 0

nodes = list(range(18))

# ==========================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ (CPM)
# ==========================================
def topological_sort(nodes, edges):
    in_degree = {n: 0 for n in nodes}
    adj = defaultdict(list)
    for u, v, _ in edges:
        adj[u].append(v)
        in_degree[v] += 1
    
    queue = deque([n for n in nodes if in_degree[n] == 0])
    topo_order = []
    while queue:
        u = queue.popleft()
        topo_order.append(u)
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
    return topo_order

def calculate_cpm(durations, edges, nodes):
    topo_order = topological_sort(nodes, edges)
    early = {n: 0 for n in nodes}
    
    # Прямой проход
    for u in topo_order:
        for eu, ev, t_name in edges:
            if eu == u:
                early[ev] = max(early[ev], early[eu] + durations[t_name])
                
    # Обратный проход
    late = {n: early[max(nodes)] for n in nodes}
    for u in reversed(topo_order):
        for eu, ev, t_name in edges:
            if eu == u:
                late[eu] = min(late[eu], late[ev] - durations[t_name])
                
    return early, late

def get_critical_path(early, late, durations, edges):
    path = []
    for u, v, t_name in edges:
        if durations[t_name] > 0 and early[u] == late[u] and early[v] == late[v] and early[v] == early[u] + durations[t_name]:
            path.append(t_name)
    return path

# ==========================================
# ЗАДАЧА 1: Метод критического пути (t_пес)
# ==========================================
early_max, late_max = calculate_cpm(durations_max, edges, nodes)
T_kr_max = early_max[max(nodes)]
crit_path_max = get_critical_path(early_max, late_max, durations_max, edges)

# ==========================================
# ЗАДАЧА 2: Вероятностные модели
# ==========================================
t_ozh = {k: (v[1] + 4*v[2] + v[3]) / 6 for k, v in tasks.items()}
t_ozh_2p = {k: (3*v[1] + 2*v[3]) / 5 for k, v in tasks.items()}
variances = {k: ((v[1] - v[3]) / 6)**2 for k, v in tasks.items()}

# 3-параметрическая модель
early_ozh, late_ozh = calculate_cpm(t_ozh, edges, nodes)
T_kr_ozh = early_ozh[max(nodes)]
crit_path_ozh = get_critical_path(early_ozh, late_ozh, t_ozh, edges)
var_kr_ozh = sum(variances[t] for t in crit_path_ozh)
sigma_ozh = math.sqrt(var_kr_ozh)

# 2-параметрическая модель
early_2p, late_2p = calculate_cpm(t_ozh_2p, edges, nodes)
T_kr_2p = early_2p[max(nodes)]
crit_path_2p = get_critical_path(early_2p, late_2p, t_ozh_2p, edges)
var_kr_2p = sum(variances[t] for t in crit_path_2p)
sigma_2p = math.sqrt(var_kr_2p)

def norm_cdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))

# Вероятности
P_ozh = norm_cdf((T_dir - T_kr_ozh) / sigma_ozh)
P_2p = norm_cdf((T_dir - T_kr_2p) / sigma_2p)

# Гарантированные интервалы (3 сигмы)
int_ozh = (T_kr_ozh - 3*sigma_ozh, T_kr_ozh + 3*sigma_ozh)
int_2p = (T_kr_2p - 3*sigma_2p, T_kr_2p + 3*sigma_2p)

# Максимальный срок с заданной надежностью (z-значение для 0.95)
z_gamma = 1.645 # Для гамма=0.95, Phi(z) = 0.45
T_max_ozh = T_kr_ozh + z_gamma * sigma_ozh
T_max_2p = T_kr_2p + z_gamma * sigma_2p

# ==========================================
# ЗАДАЧА 3: Оптимизация стоимости (Время - Стоимость)
# ==========================================
# Найдем минимально возможное время (при t_опт)
early_min, late_min = calculate_cpm(durations_opt, edges, nodes)
T_min_possible = early_min[max(nodes)]

# Линейное программирование
# Переменные: x1..x12 (сокращения), y0..y17 (времена событий)
# Индексы: x_i = 0..11, y_j = 12..29
num_tasks = len(tasks)
task_names = list(tasks.keys())
task_to_idx = {t: i for i, t in enumerate(task_names)}

# Целевая функция: минимизировать sum(s_k * x_k) + S * y_end
c = np.zeros(num_tasks + len(nodes))
for i, t in enumerate(task_names):
    c[i] = tasks[t][4]
c[num_tasks + max(nodes)] = S  # y_17

# Ограничения: y_v - y_u - x_k >= t_max_k  =>  -y_v + y_u + x_k <= -t_max_k
A_ub = []
b_ub = []

for u, v, t_name in edges:
    if t_name in tasks:
        row = np.zeros(num_tasks + len(nodes))
        row[num_tasks + u] = 1
        row[num_tasks + v] = -1
        row[task_to_idx[t_name]] = 1
        A_ub.append(row)
        b_ub.append(-durations_max[t_name])

# Ограничения на минимальное время: y_end <= T_min_possible
row = np.zeros(num_tasks + len(nodes))
row[num_tasks + max(nodes)] = 1
A_ub.append(row)
b_ub.append(T_min_possible)

# Границы: 0 <= x_k <= t_max - t_opt, y_j >= 0
bounds = [(0, durations_max[t] - durations_opt[t]) for t in task_names]
bounds += [(0, None) for _ in nodes]

# Решаем
res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

if res.success:
    opt_reductions = {t: res.x[task_to_idx[t]] for t in task_names}
    opt_durations = {t: durations_max[t] - opt_reductions[t] for t in task_names}
    min_cost = res.fun
else:
    opt_durations = durations_opt
    min_cost = float('inf')


# ==========================================
# ФОРМИРОВАНИЕ ОТЧЕТА
# ==========================================
print("="*60)
print("ЗАДАЧА 1: МЕТОД КРИТИЧЕСКОГО ПУТИ")
print("="*60)
print(f"Критическое время (T_кр) = {T_kr_max} дней.")
print(f"Критический путь: {' -> '.join(crit_path_max)}")
print("\nВременные характеристики событий:")
print(f"{'Событие':<10}{'Ранний срок Tp':<15}{'Поздний срок Tn':<15}{'Резерв R'}")
for n in nodes:
    print(f"{n:<10}{early_max[n]:<15}{late_max[n]:<15}{late_max[n]-early_max[n]}")

print("\nХарактеристики работ:")
print(f"{'Работа':<8}{'t':<5}{'ES':<5}{'EF':<5}{'LS':<5}{'LF':<5}{'Полн.рез':<10}{'Незав.рез'}")
for u, v, t_name in edges:
    if t_name in tasks:
        es = early_max[u]
        ef = early_max[u] + durations_max[t_name]
        lf = late_max[v]
        ls = late_max[v] - durations_max[t_name]
        slack_full = lf - es - durations_max[t_name]
        # Независимый резерв: Tp(v) - Tn(u) - t
        slack_indep = early_max[v] - late_max[u] - durations_max[t_name]
        print(f"{t_name:<8}{durations_max[t_name]:<5}{es:<5}{ef:<5}{ls:<5}{lf:<5}{slack_full:<10}{max(0, slack_indep)}")


print("\n" + "="*60)
print("ЗАДАЧА 2: ВЕРОЯТНОСТНЫЕ МОДЕЛИ")
print("="*60)
print("1. ТРЕХПАРАМЕТРИЧЕСКАЯ МОДЕЛЬ")
print(f"Ожидаемое критическое время (T_ож) = {T_kr_ozh:.2f} дней.")
print(f"Критический путь: {' -> '.join(crit_path_ozh)}")
print(f"Дисперсия крит. пути = {var_kr_ozh:.2f}, СКО = {sigma_ozh:.2f}")
print(f"Вероятность уложиться в {T_dir} дней: P = {P_ozh:.4f} ({P_ozh*100:.2f}%)")
print(f"Гарантированный интервал (3 сигмы): [{int_ozh[0]:.2f}; {int_ozh[1]:.2f}]")
print(f"Макс. срок с надежностью {gamma}: T = {T_max_ozh:.2f} дней")

print("\n2. ДВУХПАРАМЕТРИЧЕСКАЯ МОДЕЛЬ")
print(f"Ожидаемое критическое время (T_ож*) = {T_kr_2p:.2f} дней.")
print(f"Критический путь: {' -> '.join(crit_path_2p)}")
print(f"Дисперсия крит. пути = {var_kr_2p:.2f}, СКО = {sigma_2p:.2f}")
print(f"Вероятность уложиться в {T_dir} дней: P = {P_2p:.4f} ({P_2p*100:.2f}%)")
print(f"Гарантированный интервал (3 сигмы): [{int_2p[0]:.2f}; {int_2p[1]:.2f}]")
print(f"Макс. срок с надежностью {gamma}: T = {T_max_2p:.2f} дней")


print("\n" + "="*60)
print("ЗАДАЧА 3: ОПТИМИЗАЦИЯ СТОИМОСТИ ПРОЕКТА")
print("="*60)
print(f"Абсолютно минимально возможный срок (при всех t_опт) = {T_min_possible} дней.")
print(f"Оптимальная продолжительность работ для достижения мин. времени с мин. стоимостью:")
for t in task_names:
    print(f"{t}: {opt_durations[t]:.2f} дней (сокращено на {opt_reductions[t]:.2f})")
print(f"\nМинимальная стоимость проекта при сроке {T_min_possible} дней = {min_cost:.2f} ден. ед.")