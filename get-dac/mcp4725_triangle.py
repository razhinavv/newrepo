import mcp4725_driver as mcp
import triangle_wave as sg
import time
amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000
try:
    dac = mcp.MCP4725(3.3)
    while True:
        dac.set_voltage(amplitude * sg.get_triangle_wave_aplitude(signal_frequency, time.time()))
        sg.wait_for_sampling_period(sampling_frequency)
finally:
    dac.deinit()