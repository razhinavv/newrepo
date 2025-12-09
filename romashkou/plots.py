import matplotlib.pyplot as plt
import numpy as np


b = 0.12106135463316897
k = 0.008969825975052607

window_size = 35


def show_plot():
    plt.grid(True, alpha=.3)
    plt.xlabel("Время, с")
    plt.show()
    plt.close()
    plt.figure(figsize=(11, 8))


def cut_above_threshold(active_array, copying_array, threshold):
    active_return, copying_return = list(), list()
    for i in range(len(active_array)):
        if active_array[i] >= threshold:
            active_return.append(active_array[i])
            copying_return.append(copying_array[i])
    return active_return, copying_return


plt.figure(figsize=(11, 8))

# до нагрузки
x, y = list(), list()
with open("sidit_semen.csv") as before:
    for line in before.readlines():
        line = line.strip().split(',')
        x.append(line[0])
        y.append(line[1])
x = np.array(x, dtype='float64')
y = (np.array(y, dtype='float64') - b) / k

trend_poly = np.poly1d(np.polyfit(x, y, 5))
y_trend = trend_poly(x)
y_smooth = np.convolve(y, np.ones(window_size) / window_size, mode='same')

plt.scatter(x, y_smooth, s=1)
plt.plot(x, y_trend, color='red')
plt.ylabel("Давление, мм рт. ст.")
plt.title("Давление от времени до нагрузки")
show_plot()

y_cutted, x_cutted = cut_above_threshold(y_smooth - y_trend, x, -2)
plt.scatter(x_cutted, y_cutted, s=1)
plt.ylabel("Изменение давления, мм рт. ст.")
plt.title("Давление от времени до нагрузки, усредненное")
show_plot()

y_diff = np.gradient(y_smooth, (max(x) - min(x)) / len(x))
window_size = 40
y_diff_smooth = np.convolve(y_diff, np.ones(window_size) / window_size, mode='same')

x_min = 40.0002
x_max = 59.0009
threshold = 0
print(np.where(x == x_min)[0])
i = int(np.where(x == x_min)[0])
#j = int(np.where(x == x_max)[0])
j = 32944

k = i
times = list()
while k < j:
    if y_diff_smooth[k] >= threshold:
        k += int((j - i) * 0.05)
        times.append(x[k])
    k += 1
print(times)
print("Pulse before:", (len(times) - 1) / (times[-1] - times[0]) * 60, "bpm")

plt.scatter(x[i:j], y_diff_smooth[i:j], s=1)
plt.ylabel("dP/dt, мм рт. ст. / с")
plt.title("Давление от времени до физической активности, аппроксимированное")
show_plot()

# после нагрузки
x, y = list(), list()
with open("otzhalsa_semen.csv") as after:
    for line in after.readlines():
        line = line.strip().split(',')
        x.append(line[0])
        y.append(line[1])
x = np.array(x, dtype='float64')
y = (np.array(y, dtype='float64') - b) / k

trend_poly = np.poly1d(np.polyfit(x, y, 5))
y_trend = trend_poly(x)
y_smooth = np.convolve(y, np.ones(window_size)/window_size, mode='same')

plt.scatter(x, y_smooth, s=1, color='green')
plt.plot(x, y_trend, color='red')
plt.ylabel("Давление, мм рт. ст.")
plt.title("Давление от времени после физической активности")
show_plot()

y_cutted, x_cutted = cut_above_threshold(y_smooth - y_trend + .2, x, -2)
plt.scatter(x_cutted, y_cutted, s=1, color='black')
plt.ylabel("Изменение давления, мм рт. ст.")
plt.title("Давление от времени после нагрузки, пики")
show_plot()

y_diff = np.gradient(y_smooth, (max(x) - min(x)) / len(x))
window_size = 40
y_diff_smooth = np.convolve(y_diff, np.ones(window_size) / window_size, mode='same')

x_min = 35.0007
x_max = 55.0000
threshold = 0
print(np.where(x == x_min)[0])
i = int(np.where(x == x_min)[0])
j = int(np.where(x == x_max)[0])

k = i
times = list()
while k < j:
    if y_diff_smooth[k] >= threshold:
        k += int((j - i) * 0.05)
        times.append(x[k])
    k += 1
print("Pulse after:", (len(times) - 1) / (times[-1] - times[0]) * 60, "bpm")

plt.scatter(x[i:j], y_diff_smooth[i:j], s=1, color='green')
plt.ylabel("dP/dt, мм рт. ст.")
plt.title("Давление от времени после нагрузки, аппроксимированные пики")
show_plot()

plt.close()
