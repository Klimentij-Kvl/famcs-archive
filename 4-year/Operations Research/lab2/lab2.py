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