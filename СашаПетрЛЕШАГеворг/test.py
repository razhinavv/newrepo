import numpy as np
import matplotlib.pyplot as plt

data=np.loadtxt("./data_distance_0.txt", delimiter=',')

plt.plot(data[:,1],data[:,0])
plt.show()