import pwm_dac as pwm
import signal_generator as sg
import time
amplitude = 3.2
signal_frequency = 10
sampling_frequency = 10
try:
    dac = pwm.PWM_DAC(12, 500, 3.29)
    while True:
        dac.set_voltage(amplitude * sg.get_triangle_wave_amplitude(signal_frequency, time.time()))
        sg.wait_for_sampling_period(sampling_frequency)
finally:
    dac.deinit()