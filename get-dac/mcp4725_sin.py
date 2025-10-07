import mcp4725_driver as mcp
import signal_generator as sg
import time
amplitude = 1
signal_frequency = 1
sampling_frequency = 10
try:
    dac = mcp.MCP4725(5.1)
    start_time = time.time()
    while True:
        current_time = time.time() - start_time
        normilized_amplitude = sg.get_sin_wave_aplitude(signal_frequency, current_time)
        voltage = normilized_amplitude * amplitude
        dac.set_voltage(voltage)
        sg.wait_for_sampling_period(sampling_frequency)
finally:
    dac.deinit()