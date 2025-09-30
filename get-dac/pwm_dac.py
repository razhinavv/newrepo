import RPi.GPIO as GPIO
#import time
class PWM_DAC:
    def __init__(self, gpio_pin, pwm_frequency, dynamic_range, verbose = False):
        self.gpio_pin = gpio_pin
        self.pwm_frequency = pwm_frequency
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT, initial = 0)
        self.pwm = GPIO.PWM(self.gpio_pin,self.pwm_frequency)
        
        self.pwm.start(0)
        
        
    def deinit(self):
        self.pwm.stop()
        #GPIO.output(self.gpio_pin, 0)
        GPIO.cleanup()
    def set_voltage(self, voltage):
        if voltage < 0:
            voltage = 0
            print("Слишком мало!")
        elif voltage > self.dynamic_range:
            voltage = self.dynamic_range
            print("Слишком много!")
        duty = voltage / self.dynamic_range *100
        self.pwm.ChangeDutyCycle(duty)
if __name__ == "__main__":
    try:
        dac = PWM_DAC(12, 500, 3.29, True)
        while(True):
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)
            except ValueError:
                print("Вы ввели не число. Попробуйте еще раз\n")
    finally:
        dac = PWM_DAC(12, 500, 3.290, True)
        dac.deinit()