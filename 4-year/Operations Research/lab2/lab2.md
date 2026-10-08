
# Математическая модель

Индексы:
$i \in \{A,B\}$ — вид руды.

## Переменные

- $x_A, x_B$ — количество переработанной руды A и B, тыс. т.
- $y$ — количество продукта II, отправленного в конвертер, тыс. т.
- $b_I, b_{II}$ — закупки продукта I и II, тыс. т.
- $s_I^{1}, s_I^{2}, s_I^{3}$ — продажи продукта I по ценам 5.5, 5.2 и 5.0 у.е./т.
- $s_{II}$ — продажи продукта II, тыс. т.

## Целевая функция

Максимизировать прибыль:

$$
\begin{aligned}
\max \Pi =
& 5.5 s_I^1 + 5.2 s_I^2 + 5.0 s_I^3 + 3.8 s_{II} \\
& - 3.25 x_A - 3.40 x_B \\
& - 0.35(x_A+x_B) \\
& - 0.25 y \\
& - 0.10(0.15x_A + 0.25x_B) \\
& - 5.75 b_I - 4.0 b_{II}.
\end{aligned}
$$

Здесь $0.10(0.15x_A + 0.25x_B)$ — затраты на фильтрацию продукта I после основного процесса.

## Ограничения

Мощность основного процесса:

$$
x_A + x_B \le 100.
$$

Доступность руды:

$$
0 \le x_A \le 100, \quad 0 \le x_B \le 30.
$$

Мощность конвертера:

$$
0 \le y \le 50.
$$

Конвертер может перерабатывать только продукт II, полученный из руды:

$$
y \le 0.85x_A + 0.75x_B.
$$

Баланс продукта I:

$$
s_I^1 + s_I^2 + s_I^3 =
0.15x_A + 0.25x_B + 0.5y + b_I.
$$

Баланс продукта II:

$$
s_{II} =
0.85x_A + 0.75x_B - 0.5y + b_{II}.
$$

Ограничения на продажи продукта I:

$$
0 \le s_I^1 \le 45, \quad 0 \le s_I^2 \le 4, \quad s_I^3 \ge 0.
$$

Контракт:

$$
s_I^1 + s_I^2 + s_I^3 \ge 40.
$$

Неотрицательность всех переменных.

---

# Код AMPL + Python

```python
from amplpy import AMPL

ampl = AMPL()

ampl.eval(r"""
set ORE;

param cap_ore{ORE};
param price_ore{ORE};
param yldI{ORE};
param yldII{ORE};

param main_cap;
param main_cost;
param conv_cap;
param conv_cost;
param filt_cost_I;

param price_I_high;
param lim_I_high;
param price_I_mid;
param lim_I_mid;
param price_I_low;
param price_II;
param contract_I;
param buy_price_I;
param buy_price_II;

var x{i in ORE} integer >= 0, <= cap_ore[i];
var y integer >= 0, <= conv_cap;
var bI integer >= 0;
var bII integer >= 0;

var sI_high integer >= 0, <= lim_I_high;
var sI_mid  integer >= 0, <= lim_I_mid;
var sI_low  integer >= 0;
var sII      integer >= 0;

maximize profit:
    price_I_high * sI_high
  + price_I_mid  * sI_mid
  + price_I_low  * sI_low
  + price_II     * sII
  - sum{i in ORE} price_ore[i] * x[i]
  - main_cost * sum{i in ORE} x[i]
  - conv_cost * y
  - filt_cost_I * sum{i in ORE} yldI[i] * x[i]
  - buy_price_I * bI
  - buy_price_II * bII;

subject to main_capacity:
    sum{i in ORE} x[i] <= main_cap;

subject to I_balance:
    sI_high + sI_mid + sI_low =
        sum{i in ORE} yldI[i] * x[i] + 0.5 * y + bI;

subject to II_balance:
    sII =
        sum{i in ORE} yldII[i] * x[i] - 0.5 * y + bII;

subject to converter_feed:
    y <= sum{i in ORE} yldII[i] * x[i];

subject to contract_I_req:
    sI_high + sI_mid + sI_low >= contract_I;
""")

# Данные
ampl.set["ORE"] = ["A", "B"]

ampl.param["cap_ore"] = {"A": 100, "B": 30}
ampl.param["price_ore"] = {"A": 3.25, "B": 3.40}
ampl.param["yldI"] = {"A": 0.15, "B": 0.25}
ampl.param["yldII"] = {"A": 0.85, "B": 0.75}

ampl.param["main_cap"] = 100
ampl.param["main_cost"] = 0.35
ampl.param["conv_cap"] = 50
ampl.param["conv_cost"] = 0.25
ampl.param["filt_cost_I"] = 0.10

ampl.param["price_I_high"] = 5.50
ampl.param["lim_I_high"] = 45
ampl.param["price_I_mid"] = 5.20
ampl.param["lim_I_mid"] = 4
ampl.param["price_I_low"] = 5.00
ampl.param["price_II"] = 3.80
ampl.param["contract_I"] = 40
ampl.param["buy_price_I"] = 5.75
ampl.param["buy_price_II"] = 4.00

# Решение
ampl.option["solver"] = "highs"
ampl.solve()

# Вывод результатов
print("x_A =", ampl.var["x"]["A"].value())
print("x_B =", ampl.var["x"]["B"].value())
print("y   =", ampl.var["y"].value())
print("bI  =", ampl.var["bI"].value())
print("bII =", ampl.var["bII"].value())
print("sI_high =", ampl.var["sI_high"].value())
print("sI_mid  =", ampl.var["sI_mid"].value())
print("sI_low  =", ampl.var["sI_low"].value())
print("sII     =", ampl.var["sII"].value())
print("Прибыль =", ampl.obj["profit"].value())
```

---

# Оптимальный план

| Показатель                                                    |              Значение |
| ----------------------------------------------------------------------- | ----------------------------: |
| Руда A                                                              |                 70 тыс. т |
| Руда B                                                              |                 30 тыс. т |
| Загрузка основного процесса                    |                100 тыс. т |
| Продукт II в конвертер                                 |                 50 тыс. т |
| Продукт I после основного процесса         |                 18 тыс. т |
| Дополнительный продукт I из конвертера |                 25 тыс. т |
| Итого продукт I                                             |                 43 тыс. т |
| Продукт II к продаже                                     |                 57 тыс. т |
| Закупки продукта I                                       |                             0 |
| Закупки продукта II                                      |                             0 |
| Продажа продукта I по 5.5 у.е.                       |                 43 тыс. т |
| Продажа продукта II по 3.8 у.е.                      |                 57 тыс. т |
| **Максимальная прибыль**                       | **74.3 тыс. у.е.** |

То есть нужно переработать **70 тыс. т руды A** и **30 тыс. т руды B**, загрузив основной процесс полностью. Все 50 тыс. т продукта II, допустимые мощностью конвертера, следует отправить в конвертер. Продукт I продаётся в объёме 43 тыс. т по цене 5.5 у.е./т, продукт II — 57 тыс. т по цене 3.8 у.е./т. Контракт на 40 тыс. т продукта I выполняется, закупки не нужны.
