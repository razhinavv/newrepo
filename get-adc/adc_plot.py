import matplotlib.pyplot as plt
def plot_voltage_vs_time(time, voltage, max_voltage):
    plt.figure(figsize = (10,6))
    plt.plot(time, voltage)
    plt.xlabel("Время, с")
    plt.xlim(0, max_voltage)
    plt.ylabel("Напряжение, В")
    plt.grid('both')
    plt.legend()
    plt.title("График зависимости напряжения на входе АЦП от времени")
    plt.show()
def plot_sampling_period_hist(time):
    sampling_periods = []
    for i in range(len(time) - 1):
        sampling_periods.append(time[i+1] - time[i])
    plt.figure(figsize=(10,6))
    plt.hist(sampling_periods)
    plt.xlabel("Период измерения, с")
    plt.ylabel("Количество измерений")
    plt.title("Распределение периодов дискретизации измерений по времени на одно измерение")
    plt.xlim(0, 0.06)
    plt.grid('both')
    plt.show()