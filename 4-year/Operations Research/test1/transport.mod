
set I;
set J;

set EXISTING within I;
set NEW within I;

param cap {I} >= 0;
param demand {J} >= 0;
param c {I,J} >= 0;
param annual_cost {NEW} >= 0;

# Объемы перевозок
var x {I,J} >= 0;

# Решение о строительстве завода
var y {NEW} binary;

# Целевая функция
minimize TotalCost:
    sum {i in I, j in J} c[i,j] * x[i,j]
    + sum {i in NEW} annual_cost[i] * y[i];

# Удовлетворение спроса
subject to Demand {j in J}:
    sum {i in I} x[i,j] = demand[j];

# Ограничения действующих заводов
subject to ExistingCapacity {i in EXISTING}:
    sum {j in J} x[i,j] <= cap[i];

# Ограничения новых заводов
subject to NewCapacity {i in NEW}:
    sum {j in J} x[i,j] <= cap[i] * y[i];

# Строится ровно один новый завод
subject to ChooseOne:
    sum {i in NEW} y[i] = 1;
