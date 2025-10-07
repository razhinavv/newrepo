import r2r_dac as r2r
import triangle_wave as tw
import time
amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000
try:
    dac = r2r.R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.183)
    start_time = time.time()
    while True:
        current_time = time.time() - start_time
        normalized_amplitude = tw.get_triangle_wave_aplitude(signal_frequency, current_time)
        voltage = normalized_amplitude * amplitude
        dac.set_voltage(voltage)
        tw.wait_for_sampling_period(sampling_frequency)
finally:
    dac = r2r.R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.183)
    dac.deinit()