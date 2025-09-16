import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
leds = [16, 12, 25, 17, 27, 23, 22, 24]
GPIO.setup(leds, GPIO.OUT)
GPIO.output(leds, 0)
GPIO.setup(9, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)
num = 0
sleep_time = 0.2
def dec2bin(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]
while True:
    if GPIO.input(9) and GPIO.input(10):
        num = 2**7 - 1
        print(num, dec2bin(num))
        GPIO.output(leds, 1)
        time.sleep(sleep_time)
    elif GPIO.input(9) and num <= 2**7 - 1:
        num = num + 1
        print(num, dec2bin(num))
        for i in range(len(leds)):
            if dec2bin(num)[i] == 1:
                GPIO.output(leds[i], 1)
                time.sleep(sleep_time)
            else:
                GPIO.output(leds[i], 0)
                time.sleep(sleep_time)
    elif GPIO.input(10) and num >= 1:
        num = num - 1
        print(num, dec2bin(num))
        for i in range(len(leds)):
            if dec2bin(num)[i] == 1:
                GPIO.output(leds[i], 1)
                time.sleep(sleep_time)
            else:
                GPIO.output(leds[i], 0)
                time.sleep(sleep_time)
    