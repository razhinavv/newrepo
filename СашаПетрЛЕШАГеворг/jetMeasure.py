import jetFunctions as j
import matplotlib.pyplot as plt
import numpy as np

directionPin = 24
enablePin = 25
stepPin = 26
str=240
step=5
a=np.zeros((str,2))

j.initSpiAdc()
j.initStepMotorGpio()
for i in range (str):
    a[i,0]=(j.getAdc())
    a[i,1]=(i)
    j.stepBackward(step)
    #j.stepForward(step)
    j.time.sleep(0.2)
j.deinitSpiAdc()

with open("./data_distance_40.txt", 'w') as file:
    for i in range (str):
        file.write(f'{a[i,0]:.0f},   {a[i,1]:.0f}\n')

j.stepForward(1200)

plt.plot(a[:,1],a[:,0])
plt.show()
