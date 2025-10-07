import r2r_dac as r2r
import signal_generator as sg
import time
amplitude = 1
signal_frequency = 1
sampling_frequency = 10
try:
    dac = r2r.R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.183)
    start_time = time.time()
    while True:
        current_time = time.time() - start_time
        normalized_amplitude = sg.get_sin_wave_aplitude(signal_frequency, current_time)
        voltage = normalized_amplitude * amplitude
        dac.set_voltage(voltage)
        sg.wait_for_sampling_period(sampling_frequency)
finally:
    dac = r2r.R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.183)
    dac.deinit()