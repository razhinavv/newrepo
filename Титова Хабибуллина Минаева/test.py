import jetFunctions as j
import time
import numpy as np
import os
import csv


def save_data_to_file(data, filename):
    """Сохраняет данные в файл в формате CSV"""
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['step', 'adc_value'])
        for i, value in enumerate(data):
            writer.writerow([i, value])
    print(f"Данные сохранены в {filename}")


def get_averaged_adc(n_samples=10):
    """Возвращает усредненное значение АЦП"""
    total = 0
    for _ in range(n_samples):
        total += j.getAdc()
        time.sleep(0.01)  # небольшая задержка между измерениями
    return total / n_samples


def calibrate_adc():
    """Процедура калибровки АЦП"""
    print("\n=== Калибровка АЦП ===")

    # 1. Сбор данных при выключенном вентиляторе (нулевое давление)
    print("1. Собираем данные при выключенном вентиляторе (500 точек)...")
    j.initSpiAdc()

    # Убедимся, что вентилятор выключен
    input("Пожалуйста, убедитесь, что вентилятор выключен и нажмите Enter...")

    zero_pressure_data = []
    for i in range(500):
        if i % 50 == 0:
            print(f"Собрано {i}/500 точек...")
        zero_pressure_data.append(get_averaged_adc(5))

    save_data_to_file(zero_pressure_data, "calibration_zero.csv")
    print("Калибровочные данные при нулевом давлении сохранены!")

    # 2. Сбор данных при известном давлении
    print("\n2. Собираем данные при известном давлении (500 точек)...")

    # Инструкция пользователю
    print("Пожалуйста, подключите цифровой манометр к трубке Пито")
    print("Закройте вход вентилятора листом бумаги, чтобы не было перегрузки манометра")
    input("Включите вентилятор и нажмите Enter, когда будете готовы...")

    # Измерение давления манометром
    pressure = float(input("Введите измеренное манометром давление (Па): "))
    print(f"Собираем данные при давлении {pressure} Па...")

    known_pressure_data = []
    for i in range(500):
        if i % 50 == 0:
            print(f"Собрано {i}/500 точек...")
        known_pressure_data.append(get_averaged_adc(5))

    # Сохранение данных и давления
    save_data_to_file(known_pressure_data, "calibration_known.csv")

    # Сохранение значения давления в отдельный файл
    with open("calibration_pressure.txt", "w") as f:
        f.write(f"{pressure}")

    print(f"Калибровочные данные при давлении {pressure} Па сохранены!")
    print("Калибровка завершена!")

    j.deinitSpiAdc()
    return pressure


def measure_section(distance_mm, n_points=100):
    """Измеряет сечение струи на заданном расстоянии от сопла"""
    print(f"\nИзмерение сечения на расстоянии {distance_mm} мм от сопла")

    # Перемещение трубки Пито к начальной позиции
    # Предполагаем, что 0 мм - это центр струи
    # Нужно определить, сколько шагов соответствует 1 мм
    # Это будет зависеть от вашей установки

    # Для примера: пусть 10 шагов = 1 мм
    steps_per_mm = 10
    total_steps = 30 * steps_per_mm  # измеряем в диапазоне от -30 мм до +30 мм

    # Возвращаемся в начальную позицию (крайнее левое положение)
    j.stepBackward(total_steps)
    time.sleep(1)

    # Собираем данные
    measurements = []
    positions = []

    for i in range(n_points):
        # Вычисляем текущую позицию
        current_position = -30 + (60 * i) / (n_points - 1)
        positions.append(current_position)

        # Получаем усредненное значение АЦП
        adc_value = get_averaged_adc(5)
        measurements.append(adc_value)

        if i % 10 == 0:
            print(f"Измерено {i}/{n_points} точек, позиция: {current_position:.1f} мм")

        # Делаем шаг вправо, если не последняя точка
        if i < n_points - 1:
            j.stepForward(int(2 * steps_per_mm / (n_points - 1)))
            time.sleep(0.1)

    # Возвращаемся в начальную позицию
    j.stepBackward(total_steps)
    time.sleep(1)

    # Сохраняем данные
    filename = f"section_{distance_mm}mm.csv"
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['position_mm', 'adc_value'])
        for pos, value in zip(positions, measurements):
            writer.writerow([pos, value])

    print(f"Данные сечения сохранены в {filename}")
    return positions, measurements


def main():
    print("=== Лабораторная работа: Расход затопленной струи ===")

    # Инициализация оборудования
    j.initSpiAdc()
    j.initStepMotorGpio()

    try:
        # Калибровка
        print("\nХотите выполнить калибровку? (y/n)")
        if input().lower() == 'y':
            calibrate_adc()

        # Измерения сечений
        print("\nНачинаем измерения сечений струи...")
        input("Убедитесь, что вентилятор включен и нажмите Enter для продолжения...")

        distances = [0, 10, 20, 30, 40, 50, 60, 70]
        for distance in distances:
            measure_section(distance, n_points=100)
            print(f"Сечение на расстоянии {distance} мм измерено")
            print("Подождите 5 секунд перед следующим измерением...")
            time.sleep(5)

        print("\nВсе измерения завершены!")

    finally:
        # Очистка
        j.deinitSpiAdc()
        j.deinitStepMotorGpio()
        print("Оборудование отключено")


if __name__ == "__main__":
    main()