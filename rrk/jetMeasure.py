import jetFunctions as j
import matplotlib.pyplot as plt
import numpy as np
# calibration 0 - 84 Pa
# 10 - 82 Pa
# 20 - 75 Pa
# 30 - 68 Pa
# 40 - 25 Pa
# 50 - 27 Pa
directionPin = 24
enablePin = 25
stepPin = 26
str = 320
step = 5
a = np.zeros((str, 2))

j.initSpiAdc()
j.initStepMotorGpio()
for i in range (str):
    const = j.getAdc()
    if const > 1000000:
        a[i, 0]= a[i - 1, 0]
    else:
        a[i, 0] = const
    a[i, 1]=(i)
    j.stepBackward(step)
    #j.stepForward(step)
    j.time.sleep(0.2)
j.deinitSpiAdc()

with open("./data_distance_0_1.txt", 'w') as file:
    for i in range (str):
        file.write(f'{a[i,0]:.0f}, {a[i,1]:.0f}\n')

j.stepForward(1600)

plt.plot(a[:, 1], a[:, 0])
plt.show()
