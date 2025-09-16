import RPi.GPIO as GPIO
#import time
GPIO.setmode(GPIO.BCM)
led = 26
GPIO.setup(led, GPIO.OUT)
datchik = 6
GPIO.setup(datchik, GPIO.IN)
while True:
    GPIO.output(led,GPIO.input(datchik))
