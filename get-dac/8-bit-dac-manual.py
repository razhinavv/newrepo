import RPi.GPIO as GPIO
import time
dac_bits = [16, 20, 21, 25, 26, 17, 27, 22]
GPIO.setmode(GPIO.BCM)
GPIO.setup(dac_bits, GPIO.OUT)
dynamic_range = 3.17
def voltage_to_number(voltage):
    if not (0.0 <= voltage <= dynamic_range):
        print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {dinamic_range:.2f} B)")
        print("Устанавливаем 0.0 В")
        return 0
    return int(voltage / dynamic_range * 255)

def number_to_dac(n):
    num = [int(element) for element in bin(n)[2:].zfill(8)]
    print(num)
    sleep_time = 0.02
    for i in range(len(dac_bits)):
            if num[i] == 1:
                GPIO.output(dac_bits[i], 1)
                time.sleep(sleep_time)
            else:
                GPIO.output(dac_bits[i], 0)
                time.sleep(sleep_time)

try:
    while True:
        try:
            voltage = float(input("Введите напряжение в Вольтах: "))
            number = voltage_to_number(voltage)
            number_to_dac(number)

        except ValueError:
            print("Вы ввели не число. Попробуйте еще раз\n")
finally:
    GPIO.output(dac_bits, 0)
    GPIO.cleanup()