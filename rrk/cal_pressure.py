import numpy as np
import matplotlib.pyplot as plt

# Простой вариант для файлов с одним столбцом
no_pressure = np.loadtxt('no_pressure_processed.txt')
full_pressure = np.loadtxt('full_pressure_processed.txt')

# Средние значения
adc_no = np.mean(no_pressure)
print(adc_no)
adc_full = np.mean(full_pressure)

# Замените на реальное измеренное давление
P_measured = 84  # Па

# Расчет коэффициентов калибровки
k = P_measured / (adc_full - adc_no)
b = -k * adc_no

# Построение графика
plt.figure(figsize=(8, 6))
plt.plot([adc_no, adc_full], [0, P_measured], 'ro-', linewidth=2, markersize=8,
         label=f'Калибровочная прямая: P = {k:.4f}·ADC + {b:.4f}')
plt.plot(adc_no, 0, 'bo', markersize=6, label='Выкл. вентилятор')
plt.plot(adc_full, P_measured, 'go', markersize=6, label='Вкл. вентилятор')

plt.xlabel('Показания АЦП')
plt.ylabel('Давление, Па')
plt.title('Калибровка датчика давления')
plt.grid(True)
plt.legend()

# Добавляем аннотации к точкам
plt.annotate(f'ADC={adc_no:.1f}', (adc_no, 0), xytext=(5, 10),
             textcoords='offset points', fontsize=9)
plt.annotate(f'ADC={adc_full:.1f}', (adc_full, P_measured), xytext=(5, 10),
             textcoords='offset points', fontsize=9)

plt.tight_layout()
plt.savefig("Калибровка давления")
plt.show()

# Вывод формулы для пересчета
print(f"Формула для пересчета: P(Па) = {k:.6f} × ADC + {b:.6f}")