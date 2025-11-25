import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
steps = [0, 1000 ]
distances = [0, 5]
slope, intercept, r_value, p_value, std_err = stats.linregress(steps, distances)

mm_per_step = slope

plt.figure(figsize=(10, 6))

plt.plot(steps, distances, 'bo', markersize=8, label='Экспериментальные точки')

x_fit = np.linspace(min(steps), max(steps), 100)
y_fit = slope * x_fit + intercept
plt.plot(x_fit, y_fit, 'r-', label=f'Линейная аппроксимация: y = {slope:.4f}x + {intercept:.4f}')

plt.xlabel('Количество шагов')
plt.ylabel('Расстояние, см')
plt.title('Калибровка перемещения шагового двигателя')
plt.grid(True, alpha=0.3)
plt.legend()


for i, (s, d) in enumerate(zip(steps, distances)):
    plt.annotate(f'({s}, {d})', (s, d), xytext=(5, 5),
                 textcoords='offset points', fontsize=9)

plt.tight_layout()
plt.savefig("Калибровка шагов")
plt.show()
