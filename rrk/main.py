import numpy as np
import matplotlib.pyplot as plt
import os

# Параметры (замените на ваши реальные значения)
k = 0.0205  # Коэффициент калибровки давления: Па/ед.АЦП
adc_no = 213800  # Среднее АЦП при выключенном вентиляторе
rho = 1.2  # Плотность воздуха кг/м^3
mm_per_step = 0.25  # мм/шаг из калибровки перемещения


# Функция для преобразования АЦП в скорость
def adc_to_velocity(adc):
    P = k * (adc - adc_no)
    # Обнуляем отрицательные давления
    P[P < 0] = 0
    return np.sqrt(2 * P / rho)



def center_velocity_profile(positions, velocities):

    max_vel_index = np.argmax(velocities)
    center_position = positions[max_vel_index]
    centered_positions = positions - center_position

    return centered_positions, velocities



def calculate_flow_rate(positions, velocities):
    
    positions_m = positions / 1000
    V_times_r = velocities * np.abs(positions_m)
    integral = 0
    for i in range(len(positions_m) - 1):
        f_i = V_times_r[i]
        f_i1 = V_times_r[i + 1]
        dr = 0.00025
        integral += (f_i + f_i1) * dr / 2
    volumetric_flow = 2 * np.pi * integral
    mass_flow = volumetric_flow * rho * 1000

    return mass_flow


# Основной код
distances = [0, 10, 20, 30, 40, 50, 60, 70]  # Расстояния от сопла в мм
flow_rates = []  # Расходы для каждого сечения в г/с

# Обработка данных для каждого сечения
plt.figure(figsize=(12, 8))

for i, dist in enumerate(distances):
    # Загрузка данных из файла
    filename = f"{dist}mm.txt"

    if not os.path.exists(filename):
        print(f"Файл {filename} не найден, пропускаем...")
        continue

    # Чтение данных (предполагаем один столбец)
    data = np.loadtxt(filename)

    # Создание массива позиций
    n_points = len(data)
    positions = np.linspace(0, (n_points - 1) * mm_per_step, n_points)

    # Преобразование АЦП в скорость
    velocities = adc_to_velocity(data)

    # Центрирование профиля скорости
    centered_positions, centered_velocities = center_velocity_profile(positions, velocities)

    # Расчет расхода
    flow_rate = calculate_flow_rate(centered_positions, centered_velocities)
    flow_rates.append(flow_rate)

    # Построение профиля скорости для текущего сечения
    plt.plot(centered_positions, centered_velocities,
             label=f'{dist} мм, Q={flow_rate:.2f} г/с', linewidth=2)

# Настройка осей и сетки для первого графика
plt.xlabel('Расстояние от центра струи, мм')
plt.ylabel('Скорость, м/с')
plt.title('Профили скорости в различных сечениях струи')

# Устанавливаем основные деления каждые 10 мм и дополнительные каждые 2 мм
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(10))
plt.gca().xaxis.set_minor_locator(plt.MultipleLocator(2))

# Настраиваем сетку: основная - более заметная, дополнительная - более светлая
plt.grid(True, which='major', alpha=0.5, linestyle='-', linewidth=0.8)
plt.grid(True, which='minor', alpha=0.2, linestyle='--', linewidth=0.5)

plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig("Профили скорости")
plt.show()

# Построение графика зависимости расхода от расстояния до сопла
plt.figure(figsize=(10, 6))
plt.plot(distances[:len(flow_rates)], flow_rates, 'bo-', linewidth=2, markersize=8)
plt.xlabel('Расстояние до сопла, мм')
plt.ylabel('Массовый расход, г/с')
plt.title('Зависимость массового расхода от расстояния до сопла')

# Настройка осей и сетки для второго графика
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(10))
plt.gca().xaxis.set_minor_locator(plt.MultipleLocator(2))
plt.grid(True, which='major', alpha=0.5, linestyle='-', linewidth=0.8)
plt.grid(True, which='minor', alpha=0.2, linestyle='--', linewidth=0.5)

# Добавление значений расхода на график
for i, (dist, q) in enumerate(zip(distances[:len(flow_rates)], flow_rates)):
    plt.annotate(f'Q={q:.2f} г/с', (dist, q), xytext=(5, 5),
                 textcoords='offset points', fontsize=9)

plt.tight_layout()
plt.savefig("Расход")
plt.show()

# Вывод результатов
print("РЕЗУЛЬТАТЫ (массовый расход в г/с):")
for i, (dist, q) in enumerate(zip(distances[:len(flow_rates)], flow_rates)):
    print(f"Расстояние {dist} мм: расход = {q:.2f} г/с")