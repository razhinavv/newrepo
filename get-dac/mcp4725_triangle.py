import mcp4725_driver as mcp
import triangle_wave as sg
import time
amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000
try:
    dac = mcp.MCP4725(3.3)
    start_time = time.time()
    while True:
        current_time = time.time() - start_time
        normilized_amplitude = sg.get_triangle_wave_aplitude(signal_frequency, current_time) / 2
        voltage = normilized_amplitude * amplitude
        dac.set_voltage(voltage)
        sg.wait_for_sampling_period(sampling_frequency)
finally:
    dac.deinit()