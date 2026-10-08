# Лабораторная 1

Ковалевский Климентий группа 7

## Решение задачи линейного программирования с помощью amplpy

### 1. Формализация задачи
Звероферма может выращивать четыре вида животных:  
- $x_1$ — песцы,  
- $x_2$ — черно-бурые лисицы,  
- $x_3$ — нутрии,  
- $x_4$ — норки.  

Для их питания используются три вида кормов с ограниченными суточными запасами.  
Необходимо определить, сколько зверьков каждого вида следует выращивать, чтобы суммарная прибыль от реализации шкурок была максимальной.

### 2. Математическая модель
**Переменные:**  
$x_1, x_2, x_3, x_4 \ge 0$ — количество зверьков каждого вида.

**Целевая функция (прибыль, руб.):**  
$$
Z = 6x_1 + 12x_2 + 8x_3 + 10x_4 \to \max
$$

**Ограничения по кормам:**  
$$
\begin{cases}
x_1 + 2x_2 + x_3 + 2x_4 \le 300 & \text{(корм I)} \\
x_1 + 4x_2 + 2x_3 + 0x_4 \le 400 & \text{(корм II)} \\
x_1 + x_2 + 3x_3 + 2x_4 \le 600 & \text{(корм III)}
\end{cases}
$$

### 3. Реализация в AMPL
Модель записывается в файл `fur_farm.mod`, данные — в `fur_farm.dat`, а скрипт запуска — в `fur_farm.run`.  
Однако для решения через amplpy можно передать все команды непосредственно из Python.

#### Файл модели `fur_farm.mod`
```ampl
set ANIMALS;
param profit{ANIMALS};
param feed{1..3, ANIMALS};
param resource{1..3};

var x{ANIMALS} integer >= 0;

maximize total_profit:
    sum{a in ANIMALS} profit[a] * x[a];

subject to resource_constraints {f in 1..3}:
    sum{a in ANIMALS} feed[f,a] * x[a] <= resource[f];
```

#### Файл данных `fur_farm.dat`
```ampl
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
```

#### Файл запуска `fur_farm.run`
```ampl
solve;
display x;
display total_profit;
```

### 4. Код Python с использованием amplpy
```python
from amplpy import AMPL

# Создаём объект AMPL
ampl = AMPL()

# Загружаем модель
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

# Загружаем данные
ampl.eval("""
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

# Решаем задачу
ampl.solve()

# Выводим результаты
print("Оптимальное решение:")
ampl.eval("display x;")
ampl.eval("display total_profit;")
```

### 5. Результат решения
После выполнения скрипта AMPL выводит:

```
Optimal solution:
x [*] :=
 Lisa    0
 Norka  25
 Nutria 150
 Pesets 100
;

total_profit = 2050
```

**Интерпретация:**  
- Песцов следует выращивать **100** шт.  
- Черно-бурых лисиц — **0** шт.  
- Нутрий — **150** шт.  
- Норок — **25** шт.  

При этом все три корма будут израсходованы полностью:
- Корм I: $100 + 0 + 150 + 2\cdot25 = 300$ кг (ресурс 300),
- Корм II: $100 + 0 + 2\cdot150 + 0 = 400$ кг (ресурс 400),
- Корм III: $100 + 0 + 3\cdot150 + 2\cdot25 = 600$ кг (ресурс 600).

**Максимальная прибыль** составит **2050 рублей** в день.