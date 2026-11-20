
from amplpy import AMPL

# Создание экземпляра AMPL
ampl = AMPL()

# Загрузка математической модели
ampl.read("transport.mod")

# Загрузка исходных данных
ampl.readData("transport.dat")

# Выбор оптимизационного решателя
ampl.eval("option solver highs;")

# Решение задачи
ampl.solve()

# Вывод результатов
print("Оптимальное значение целевой функции:")
ampl.eval("display TotalCost;")

print("Решение о строительстве:")
ampl.eval("display y;")

print("Оптимальные объемы перевозок:")
ampl.eval("display x;")
