import mcp4725_driver as mcp
import signal_generator as sg
import time
amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000
try:
    dac = mcp.MCP4725(5.1)
    while True:
        
        dac.set_voltage(amplitude * sg.get_sin_wave_aplitude(signal_frequency, time.time()))
        sg.wait_for_sampling_period(sampling_frequency)
finally:
    dac.deinit()