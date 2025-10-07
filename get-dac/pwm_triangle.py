import pwm_dac as pwm
import triangle_wave as sg
import time
amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000
try:
    dac = pwm.PWM_DAC(12, 500, 3.29)
    start_time = time.time()
    while True:
        timee = time.time() - start_time
        normilized_amplitude = sg.get_triangle_wave_aplitude(signal_frequency, timee) / 2
        voltage = normilized_amplitude * amplitude
        dac.set_voltage(voltage)
        sg.wait_for_sampling_period(sampling_frequency)
finally:
    dac.deinit()