from amplpy import AMPL

# Создаем объект AMPL
ampl = AMPL()

# 1. Загружаем модель (только объявления)
ampl.eval("""
set ANIMALS;
param profit{ANIMALS};
param feed{1..3, ANIMALS};
param resource{1..3};

var x{ANIMALS} integer >= 0;

maximize total_profit:
    sum{a in ANIMALS} profit[a] * x[a];

subject to resource_constraints {f in 1..3}:
    sum{a in ANIMALS} feed[f,a] * x[a] <= resource[f];
""")

# 2. Загружаем данные (режим data)
ampl.eval("""
data;
set ANIMALS := Pesets Lisa Nutria Norka;

param profit :=
    Pesets 6
    Lisa   12
    Nutria 8
    Norka  10;

param resource :=
    1 300
    2 400
    3 600;

param feed: Pesets Lisa Nutria Norka :=
    1   1   2   1   2
    2   1   4   2   0
    3   1   1   3   2;
""")

# 3. Выбор решателя
ampl.eval("option solver highs;")

# 4. Решение
ampl.solve()

# 5. Вывод результатов
print("Оптимальное решение:")
ampl.eval("display x;")
ampl.eval("display total_profit;")