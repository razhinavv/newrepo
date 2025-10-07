import numpy as np
import time
def get_sin_wave_aplitude(freq, time):
    sin_value = np.sin(2 * np.pi * freq * time) + 1
    normilized_value = sin_value / 2
    return normilized_value
def wait_for_sampling_period(sampling_frequency):
    sampling_period = 1.0 / sampling_frequency
    time.sleep(sampling_period)