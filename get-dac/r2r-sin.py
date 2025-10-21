import r2r_dac as r2r
import signal_generator as sg
import time
amplitude = 1
signal_frequency = 1
sampling_frequency = 10
try:
    dac = r2r.R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.183, True)
    
    while True:
        dac.set_voltage(amplitude * sg.get_sin_wave_aplitude(signal_frequency, time.time()))
        sg.wait_for_sampling_period(sampling_frequency)
finally:
    dac = r2r.R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.183)
    dac.deinit()