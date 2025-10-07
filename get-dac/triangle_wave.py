import time
def get_triangle_wave_aplitude(freq, time):
    period = 1.0 / freq
    triangle_value = (time % period) / period
    if triangle_value < 0.5:
        normilized_value =  triangle_value * 2
    else:
        normilized_value = 2 * (1 - triangle_value)
    return normilized_value
def wait_for_sampling_period(sampling_frequency):
    sampling_period = 1.0 / sampling_frequency
    time.sleep(sampling_period)