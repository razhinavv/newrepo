import RPi.GPIO as GPIO
#import time
GPIO.setmode(GPIO.BCM)
led = 26
#leds = [24, 22, 23, 27, 17, 25, 12, 16]
#GPIO.setup(leds, GPIO.OUT)
GPIO.setup(led, GPIO.OUT)
datchik = 6
GPIO.setup(datchik, GPIO.IN)
while True:
    GPIO.output(led,GPIO.input(datchik))
