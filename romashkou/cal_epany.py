import matplotlib.pyplot as plt
import numpy as np


def print_equation(coefficients):
    print("> equation:", end=' ')
    n = len(coefficients)
    print(' + '.join(f"({coefficients[i]})x^{n - i - 1}" for i in range(len(coefficients))))


averages = list()
real_values = (40, 80, 120, 160, 200)
for num in real_values:
    with open(f"cal{num}.csv") as f:
        all_lines = f.readlines()
        averages.append(sum(list(map(lambda s: float(s.split(',')[1]), all_lines))) / len(all_lines))

x = np.array(real_values, dtype='float64')
y = np.array(averages, dtype='float64')

delta = max(x) - min(x)
x_fit = np.linspace(min(x) - 2 * delta, max(x) + 2 * delta, 1000)
y_fits = list()

print("selected equations:")
coeffs = list()
for deg in range(1, 4):
    print(f"> deg: {deg}")
    coeffs.append(np.polyfit(x, y, deg))
    print_equation(coeffs[-1])
    polynom_function = np.poly1d(coeffs[-1])
    y_fits.append(polynom_function(x_fit))
    print()


plt.figure(figsize=(11, 8))
for deg in range(2):
    plt.scatter(x_fit, y_fits[deg], label=f"Интерполяция, степень {deg+1}", s=1)
plt.scatter(x, y, label='Снятые точки', s=15)

plt.title("Калибровка")
plt.xlabel("Давление, мм рт. ст.")
plt.ylabel("Напряжение, В")
plt.legend()
plt.grid(True, alpha=.3)
plt.show()
