import r2r_adc as r2r
import time
import adc_plot as plot
adc = r2r.R2R_ADC(3.290)
voltage_values = []
time_values = []
duration = 3.0
try:
    start = time.time()
    current_time = start
    while current_time - start < duration:
        voltage_values.append(adc.get_sar_voltage())
        time_values.append(current_time - start)
        current_time = time.time()
        time.sleep(0.005)
    plot.plot_voltage_vs_time(time_values, voltage_values, 3.290)
    plot.plot_sampling_period_hist(time_values)
    print(len(time_values), len(voltage_values))
finally:
    adc.deinit()