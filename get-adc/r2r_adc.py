import RPi.GPIO as GPIO
import time
class R2R_ADC:
    def __init__(self, dynamic_range, compare_time = 0.001, verbose = False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time

        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial = 0)
        GPIO.setup(self.comp_gpio, GPIO.IN)
    def deinit(self):
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()
    def number_to_dac(self, number):
        return [int(element) for element in bin(number)[2:].zfill(8)]
    def sequential_counting_adc(self):
        maxnum = 255
        for i in range(256):
            GPIO.output(self.bits_gpio, self.number_to_dac(i))
            time.sleep(self.compare_time)
            if GPIO.input(self.comp_gpio):
                if self.verbose:
                    print(f"компаратор сработал {i}")
                return i
        #if self.verbose:
        print(f"максимально можно подать {255}")
        return maxnum
    def get_sc_voltage(self):
        number = self.sequential_counting_adc()
        voltage = self.dynamic_range * number / (255)
        return voltage
    def successive_approximation_adc(self):
        value = 0
        for bit in [128, 64, 32, 16, 8, 4, 2, 1]:
            maybe_value = value | bit
            GPIO.output(self.bits_gpio, self.number_to_dac(maybe_value))
            comp = GPIO.input(self.comp_gpio)
            time.sleep(0.001)
            if comp == 0:
                value = maybe_value
        GPIO.output(self.bits_gpio, 0)
        return value
        
    def get_sar_voltage(self):
        number = self.successive_approximation_adc()
        voltage = self.dynamic_range * number / 255
        return voltage
if __name__ == "__main__":
    adc = R2R_ADC(3.160, 0.01, False)
    try:
        
        while True:
            voltage = adc.get_sc_voltage()
            print(f"Напряжение {voltage} B")
    finally:
        #adc = R2R_ADC(3.160, 0.01, False)
        adc.deinit()