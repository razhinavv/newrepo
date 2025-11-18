# newrepo
инженерная подготовка

import time
import numpy as np
import jetFunctions as j
import RPi.GPIO as GPIO

def setup_spi():
    """Настройка SPI для работы с АЦП"""
    print("Настройка SPI...")
    # Выполняем команды для настройки GPIO пинов в терминале:
    # raspi-gpio set 9 a0
    # raspi-gpio set 10 a0  
    # raspi-gpio set 11 a0
    j.initSpiAdc()

def calibrate_pressure_off():
    """Калибровка при выключенном вентиляторе"""
    print("Калибровка: выключите вентилятор и нажмите Enter")
    input()
    
    adc_values = []
    for i in range(500):
        adc_value = j.getAdc()
        adc_values.append(adc_value)
        if i % 50 == 0:
            print(f"Измерение {i}/500")
    
    np.savetxt('calibration_pressure_off.txt', adc_values)
    print("Калибровка при выключенном вентиляторе завершена")

def calibrate_pressure_on():
    """Калибровка при включенном вентиляторе"""
    print("Калибровка: включите вентилятор, закройте вход листком бумаги")
    print("Измерьте давление цифровым манометром и нажмите Enter")
    input()
    
    adc_values = []
    for i in range(500):
        adc_value = j.getAdc()
        adc_values.append(adc_value)
        if i % 50 == 0:
            print(f"Измерение {i}/500")
    
    np.savetxt('calibration_pressure_on.txt', adc_values)
    print("Калибровка при включенном вентиляторе завершена")

def measure_section(distance_mm, points=100):
    """Измерения в одном сечении струи"""
    print(f"Измерение в сечении {distance_mm} мм от сопла")
    
    # Перемещение трубки Пито в нужное сечение
    # Здесь нужно реализовать логику перемещения на заданное расстояние
    # Для простоты будем считать, что мы знаем количество шагов на мм
    steps_per_mm = 10  # Это значение нужно определить экспериментально
    steps_needed = distance_mm * steps_per_mm
    
    if steps_needed > 0:
        j.stepForward(steps_needed)
    elif steps_needed < 0:
        j.stepBackward(abs(steps_needed))
    
    time.sleep(1)  # Пауза для стабилизации
    
    # Измерение в поперечном направлении
    adc_values = []
    for i in range(points):
        adc_value = j.getAdc()
        adc_values.append(adc_value)
        
        # Перемещение на один шаг для следующего измерения
        j.stepForward(1)
        
        if i % 20 == 0:
            print(f"Точка {i}/{points}")
    
    # Сохранение данных
    filename = f'section_{distance_mm}mm.txt'
    np.savetxt(filename, adc_values)
    print(f"Данные для сечения {distance_mm} мм сохранены в {filename}")
    
    # Возврат в начальное положение
    j.stepBackward(points)  # Возвращаемся назад на points шагов

def main():
    """Основная функция измерения"""
    try:
        # Инициализация
        setup_spi()
        j.initStepMotorGpio()
        
        print("Лабораторная работа: Измерение затопленной струи")
        print("=" * 50)
        
        # Калибровка
        print("Этап 1: Калибровка давления")
        calibrate_pressure_off()
        calibrate_pressure_on()
        
        # Измерения в сечениях
        print("\nЭтап 2: Измерения в сечениях струи")
        distances = [0, 10, 20, 30, 40, 50, 60, 70]
        
        for distance in distances:
            measure_section(distance, points=100)
            print(f"Завершены измерения в сечении {distance} мм")
        
        print("\nВсе измерения завершены!")
        
    except KeyboardInterrupt:
        print("\nИзмерения прерваны пользователем")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        # Корректное завершение
        j.deinitSpiAdc()
        j.deinitStepMotorGpio()
        print("Ресурсы освобождены")

if __name__ == "__main__":
    main()
