import RPi.GPIO as GPIO
import time
class R2R_DAC:
    def __init__(self, gpio_bits, dynamic_range, verbose = False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT, initial = 0)
    def deinit(self):
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()
    def set_voltage(self, voltage):
        number = int(voltage / self.dynamic_range * 255)
        self.set_number(number)
    def set_number(self, number):
        num = [int(element) for element in bin(number)[2:].zfill(8)]
        print(num)
        sleep_time = 0.02
        for i in range(len(self.gpio_bits)):
            if num[i] == 1:
                GPIO.output(self.gpio_bits[i], 1)
                time.sleep(sleep_time)
            else:
                GPIO.output(self.gpio_bits[i], 0)
                time.sleep(sleep_time)
    
if __name__ == "__main__":
    try:
        dac = R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.177, True)

        while(True):
            try:
                voltage = float(input("Введите напрядение в Вольтах: "))
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте еще раз\n")
    finally:
        dac = R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.177, True)
        dac.deinit()