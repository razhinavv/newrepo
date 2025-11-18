import jetFunctions as jet
import time
from matplotlib import pyplot as plt
import csv

try:
    steps = 0

    jet.initStepMotorGpio()

    while True:
        n = input('Enter steps or command (h - help) > ')

        if n == 'h':
            print('\nHelp for "Jet Mover":')
            print('     50 - positive integer to step forward')
            print('    -80 - negative integer to step backward')
            print('      s - actual position relative to zero')
            print('      z - set zero')
            print('      q - exit')
            print('Try in now!\n')

        elif n == 's':
            print(steps, ' steps')

        elif n == 'z':
            steps = 0
            print(steps, ' steps')

        elif n == 'q':
            print(steps, ' steps')
            break

        else:
            jet.initSpiAdc()
            n = int(n)
            with open('data.csv', 'w') as file:
                for i in range(abs(n)):
                    file.write(str(jet.getAdc()))
                    file.write('\n')
                    time.sleep(0.015)
                    if n < 0:
                        jet.stepBackward(abs(1))
                    if n > 0:
                        jet.stepForward(1)
            steps += n
            jet.deinitSpiAdc()

finally:
    jet.deinitStepMotorGpio()