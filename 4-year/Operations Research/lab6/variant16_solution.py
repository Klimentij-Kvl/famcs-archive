"""Лабораторная работа № 6, вариант 16.

Решение задачи о максимальном паросочетании и задачи о назначениях.
Зависимости: networkx, scipy, numpy, matplotlib.
Установка: python -m pip install networkx scipy numpy matplotlib
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from scipy.optimize import linear_sum_assignment


# ---------------------------------------------------------------------------
# 1. Максимальное паросочетание и минимальное вершинное покрытие
# ---------------------------------------------------------------------------

TOP = [6, 7, 8, 9, 10, 11, 12]
BOTTOM = [0, 1, 2, 3, 4, 5]

# Рёбра графа варианта 16 (считаны с рисунка на странице 4 методички).
EDGES = [
    (6, 2), (6, 3),
    (7, 1), (7, 5),
    (8, 0), (8, 3),
    (9, 0), (9, 2), (9, 4),
    (10, 3), (10, 4),
    (11, 1), (11, 5),
    (12, 3), (12, 5),
]

G = nx.Graph()
G.add_nodes_from(TOP, bipartite=0)
G.add_nodes_from(BOTTOM, bipartite=1)
G.add_edges_from(EDGES)

# Явное паросочетание-свидетельство. Все пары являются рёбрами графа,
# и все вершины в каждой доле попарно не повторяются.
MATCHING = [
    (6, 2),
    (7, 1),
    (8, 0),
    (10, 4),
    (11, 5),
    (12, 3),
]

assert all(G.has_edge(u, v) for u, v in MATCHING)
assert len({u for u, _ in MATCHING}) == len(MATCHING)
assert len({v for _, v in MATCHING}) == len(MATCHING)

# Проверяем алгоритмом NetworkX, что размер максимального паросочетания равен 6.
matching_dict = nx.algorithms.bipartite.maximum_matching(G, top_nodes=TOP)
maximum_matching_size = len(matching_dict) // 2
assert maximum_matching_size == 6
assert len(MATCHING) == maximum_matching_size

# Все вершины нижней доли образуют вершинное покрытие: каждое ребро
# двудольного графа имеет один конец в нижней доле.
VERTEX_COVER = set(BOTTOM)
assert all(u in VERTEX_COVER or v in VERTEX_COVER for u, v in G.edges)
assert len(VERTEX_COVER) == maximum_matching_size

# Проверка минимальности покрытия по теореме Кёнига:
# размер минимального вершинного покрытия равен размеру максимального паросочетания.
minimum_vertex_cover_size = len(VERTEX_COVER)
assert minimum_vertex_cover_size == maximum_matching_size

print("Задача 1")
print("Максимальное паросочетание:", MATCHING)
print("Размер максимального паросочетания:", maximum_matching_size)
print("Минимальное вершинное покрытие:", sorted(VERTEX_COVER))
print("Размер минимального вершинного покрытия:", minimum_vertex_cover_size)

# Схема графа с выделенным паросочетанием и вершинным покрытием.
fig, ax = plt.subplots(figsize=(10, 4.7))
positions = {v: (i, 1) for i, v in enumerate(TOP)}
positions.update({v: (i + 0.5, 0) for i, v in enumerate(BOTTOM)})

matched_set = set(MATCHING)
non_matched = [e for e in EDGES if e not in matched_set]
nx.draw_networkx_edges(
    G, positions, edgelist=non_matched, ax=ax,
    width=1.4, edge_color="#8b929b", alpha=0.85,
)
nx.draw_networkx_edges(
    G, positions, edgelist=MATCHING, ax=ax,
    width=3.0, edge_color="#c43c39",
)
node_colors = ["#f6d6a8" if v in VERTEX_COVER else "#b9d9ee" for v in G.nodes]
nx.draw_networkx_nodes(
    G, positions, nodelist=list(G.nodes), node_color=node_colors,
    edgecolors="#2d6f9f", linewidths=1.4, node_size=800, ax=ax,
)
nx.draw_networkx_labels(G, positions, font_size=11, font_weight="bold", ax=ax)
ax.set_title("Вариант 16: максимальное паросочетание", fontsize=13, pad=14)
ax.axis("off")
fig.tight_layout()
fig.savefig(Path(__file__).with_name("variant16_graph.png"), dpi=200, bbox_inches="tight")
plt.close(fig)


# ---------------------------------------------------------------------------
# 2. Задача о назначениях
# ---------------------------------------------------------------------------

COST = np.array(
    [
        [1, 1, 4, 5, 7],
        [4, 5, 2, 1, 3],
        [4, 7, 2, 2, 5],
        [5, 7, 6, 9, 1],
        [2, 6, 3, 1, 7],
    ],
    dtype=int,
)

row_ind, col_ind = linear_sum_assignment(COST)
assignment = [(int(i + 1), int(j + 1), int(COST[i, j])) for i, j in zip(row_ind, col_ind)]
minimum_cost = int(COST[row_ind, col_ind].sum())

# Двойственные оценки, позволяющие независимо подтвердить оптимальность.
# Для всех i,j выполнено COST[i,j] >= U[i] + V[j].
U = np.array([0, 1, 2, 0, 1], dtype=int)
V = np.array([1, 1, 0, 0, 1], dtype=int)
REDUCED = COST - U[:, None] - V[None, :]

assert np.all(REDUCED >= 0)
assert int(U.sum() + V.sum()) == minimum_cost == 7
assert np.all(REDUCED[row_ind, col_ind] == 0)

print("\nЗадача 2")
print("Матрица стоимостей:\n", COST)
print("Оптимальное назначение (работник, работа, стоимость):", assignment)
print("Перестановка:", tuple(j for _, j, _ in assignment))
print("Минимальная суммарная стоимость:", minimum_cost)
print("Двойственные оценки U:", U.tolist())
print("Двойственные оценки V:", V.tolist())
print("Матрица приведённых стоимостей:\n", REDUCED)
