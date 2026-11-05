import amplpy
from amplpy import AMPL

# ==========================================
# 1. Инициализация и загрузка модели AMPL
# ==========================================
ampl = AMPL()
ampl.eval("""
set ACTS;                     # Множество работ
set PREC within {ACTS, ACTS}; # Отношения предшествования

param t_min {ACTS};           # t_опт (минимальная продолжительность)
param t_max {ACTS};           # t_пес (максимальная продолжительность)
param s {ACTS};               # Стоимость сокращения на 1 день
param S_cost;                 # Стоимость одного дня проекта

var S {ACTS} >= 0;            # Время начала работ
# ИСПРАВЛЕНИЕ: добавлено {a in ACTS} для корректного задания границ
var t {a in ACTS} >= t_min[a], <= t_max[a]; 
var T >= 0;                   # Общее время проекта

# Целевые функции
minimize TotalCost:
    S_cost * T + sum {a in ACTS} s[a] * (t_max[a] - t[a]);

minimize CrashCost:
    sum {a in ACTS} s[a] * (t_max[a] - t[a]);

# Ограничения
subject to Precedence {(a,b) in PREC}:
    S[b] >= S[a] + t[a];

subject to ProjectTime {a in ACTS}:
    T >= S[a] + t[a];
""")

# ==========================================
# 2. Ввод данных для Варианта 16
# ==========================================
activities = ['b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'b10', 'b11', 'b12']

# Зависимости (предшествование)
prec_data = [
    ('b1', 'b4'), ('b2', 'b5'), ('b2', 'b6'),
    ('b3', 'b7'), ('b6', 'b7'),
    ('b7', 'b8'), ('b7', 'b9'),
    ('b4', 'b10'), ('b5', 'b10'), ('b8', 'b10'),
    ('b9', 'b11'), ('b10', 'b11'),
    ('b4', 'b12'), ('b5', 'b12')
]

t_min = {'b1': 3, 'b2': 4, 'b3': 2, 'b4': 4, 'b5': 6, 'b6': 2, 'b7': 3, 'b8': 1, 'b9': 4, 'b10': 3, 'b11': 7, 'b12': 8}
t_max = {'b1': 15, 'b2': 10, 'b3': 14, 'b4': 11, 'b5': 16, 'b6': 9, 'b7': 8, 'b8': 9, 'b9': 12, 'b10': 11, 'b11': 13, 'b12': 16}
s_cost = {'b1': 9, 'b2': 5, 'b3': 7, 'b4': 3, 'b5': 6, 'b6': 5, 'b7': 10, 'b8': 9, 'b9': 7, 'b10': 6, 'b11': 11, 'b12': 8}

# Загрузка данных в AMPL
ampl.set['ACTS'] = activities
ampl.set['PREC'] = prec_data
ampl.param['t_min'] = t_min
ampl.param['t_max'] = t_max
ampl.param['s'] = s_cost
ampl.param['S_cost'] = 14

# ==========================================
# 3. Фаза 1: Поиск оптимального по стоимости варианта
# ==========================================
ampl.eval("drop CrashCost;")
ampl.eval("minimize TotalCost;")
ampl.solve()

print("=== Фаза 1: Оптимальный вариант по стоимости ===")
print(f"Оптимальное время выполнения T = {ampl.get_value('T')} дней")
print(f"Минимальная общая стоимость = {ampl.get_value('TotalCost'):.2f} ден. ед.")
print("Продолжительности работ:")
for a in activities:
    print(f"  {a}: t = {ampl.var['t'][a].value():.1f}")

# ==========================================
# 4. Фаза 2: Минимизация стоимости при минимально возможном сроке
# ==========================================
# Сначала найдем минимально возможное время выполнения проекта (T_min)
ampl.eval("drop TotalCost;")
ampl.eval("minimize T_min_obj: T;")
ampl.solve()
T_min = ampl.get_value('T')
print(f"\nМинимально возможное время выполнения T_min = {T_min} дней")

print(f"\n=== Фаза 2: Минимизация стоимости при T_min = {T_min} дней ===")
# Меняем целевую функцию на минимизацию затрат на сокращение
ampl.eval("drop T_min_obj;")
ampl.eval("minimize CrashCost;")
# Добавляем ограничение на фиксированное время
ampl.eval(f"subject to FixTime: T <= {T_min};")
ampl.solve()

crash_cost = ampl.get_value('CrashCost')
total_cost_min_time = crash_cost + 14 * T_min

print(f"Зафиксированное время T = {ampl.get_value('T')} дней")
print(f"Затраты на дополнительное сокращение (S_доп) = {crash_cost:.2f} ден. ед.")
print(f"Итоговая стоимость (14 * {T_min} + S_доп) = {total_cost_min_time:.2f} ден. ед.")
print("Оптимальные продолжительности работ при минимальном сроке:")
for a in activities:
    t_val = ampl.var['t'][a].value()
    # Помечаем работы, которые были сокращены до минимума
    status = " (макс. интенсивность)" if abs(t_val - t_min[a]) < 1e-5 else ""
    print(f"  {a}: t = {t_val:.1f}{status}")