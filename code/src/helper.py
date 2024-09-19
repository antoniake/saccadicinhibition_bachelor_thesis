import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from math import atan2, degrees

# convert from csv to tsc and extract X_POS_SCREEN and Y_POS_SCREEN without header for remodnav

def convert_tsv(filename):
    filename=filename
    file = pd.read_csv(f'{filename}',escapechar='\n')
    file = file[['X_POS_SCREEN','Y_POS_SCREEN']]
    new_filename = filename.split(".csv")[0]
    file.to_csv(f'{new_filename}.tsv', sep='\t', header=None, encoding=None, index=False)
    
    return os.path.abspath(f'{new_filename}.tsv')

# calculate velocity for each trial and set threshold with noise_factor for remodnav

def show_velocity_threshold_for_one_file(input_file, column_x, column_y, column_t, noise_factor):
    x, y, t = get_coordinates(input_file, column_x, column_y, column_t)
    velocity = get_velocity(x, y, t)
    median_noise = get_median_noise(velocity)
    threshold = median_noise * noise_factor
    show_figure(velocity, threshold)
    # shows a figure

def get_velocity(x, y, t):
    assert len(x) == len(y) == len(t)
    velocity = []
    for pos in range(0,len(x)-1):
        x1 = x[pos]
        x2 = x[pos+1]
        y1 = y[pos]
        y2 = y[pos+1]
        t1 = t[pos]
        t2 = t[pos+1]
        vel = np.sqrt((x2 - x1)**2 + (y2 - y1)**2) / (t2-t1)
        velocity.append(vel)
    return velocity 

def get_coordinates(input_file, column_x, column_y, column_t):
    file = pd.read_csv(input_file)
    x = file[column_x]
    y = file[column_y]
    t = file[column_t]
    return x, y, t 

def get_median_noise(velocity):
   return np.nanmedian(velocity)


def show_figure(velocity, threshold):
    plt.plot(velocity, color = 'pink')
    plt.hlines(threshold, 0, len(velocity))
    plt.ylim([0,2000])
    plt.show()
    
# calculate scaling factor from viewing distance, screen resolution and screen size for remodnav

def get_viewing_distance(df):
    #print(df.head())
    #print(df.columns)
    #print(df['VIEWING_DISTANCE'])
    return np.nanmedian(df['VIEWING_DISTANCE'])

def scaling_func(distance, screen_size=508, resolution=1920/508):
    angle = degrees(atan2(0.5 * screen_size, distance))
    scaling_factor = angle / (0.5 * resolution)
    return 1/scaling_factor

# causal rate analysis
def causal_rate(move_onset, lock_window_start, lock_window_end, n_trials, alpha):
    """
     analyse rate in causal time window

     input:    move_onset  - movement onset times
               lock_window_start  - window before lock
               lock_window_end  - window after lock
               n_trials      - number of trials

     output:   rate    - movement rate
               scale   - time axis

    12.12.2005 by Martin Rolfs
    21.06.2021 translated to python by Clara Kuper
    """
    scale = np.arange(lock_window_start, lock_window_end, 1)
    # check how many trials these values came from
    if type(n_trials) == int:
        n_trials = np.linspace(n_trials, n_trials, len(scale))
    elif len(n_trials) != len(scale):
        raise ValueError('n_trials must have the same as the length of lock_window_start:lock_window_end!'
                         f'But has length {len(n_trials)} instead of {len(scale)}')
    # alpha defines how much the distribution is shifted
    alpha = alpha
    # define empty arrays for scale and rate
    rate = []
    raw_rate = []

    # loop through all time windows
    for idx, t in enumerate(scale):
        # compute tau
        # here is a filter for all events BEFORE time point t
        tau = t - move_onset + 1 / alpha
        # filter tau as event 0/1
        tau = tau[tau > 0]
        # get the number of saccades in a given window
        causal = alpha ** 2 * tau * np.exp(-alpha * tau)
        # save the rate
        rate.append(sum(causal) * 1000 / n_trials[idx])
        raw_rate.append(sum(causal) * 1000)
    return np.array(raw_rate), np.array(rate), scale

def get_indices_by_value(scale, start_value, end_value):
    start_index = np.where(scale == start_value)[0]
    end_index = np.where(scale == end_value)[0]
    assert len(start_index) == len(end_index) == 1
    return start_index[0], end_index[0]

def get_mean_between_indices(rate, start_index, end_index):
    rate_window = rate[start_index : end_index]
    #print(rate_window)
    return np.mean(rate_window)

def get_mean_between_values(scale, rate, start_value, end_value):
    start_index, end_index = get_indices_by_value(scale, start_value, end_value)
    return get_mean_between_indices(rate, start_index, end_index)

def get_minimum_between_indices(rate, start_index, end_index):
    rate_window = rate[start_index : end_index]
    #print(rate_window)
    return np.min(rate_window)

def get_minimum_between_values(scale, rate, start_value, end_value):
    start_index, end_index = get_indices_by_value(scale, start_value, end_value)
    return get_minimum_between_indices(rate, start_index, end_index)

def get_maximum_between_indices(rate, start_index, end_index):
    rate_window = rate[start_index : end_index]
    #print(rate_window)
    return np.max(rate_window)

def get_maximum_between_values(scale, rate, start_value, end_value):
    start_index, end_index = get_indices_by_value(scale, start_value, end_value)
    return get_maximum_between_indices(rate, start_index, end_index)


def get_rates_for_normalization(all_rates_to_normalize, all_rates_to_normalize_by, participant_id):
    rate_to_normalize = all_rates_to_normalize[participant_id]
    rates_to_normalize_by = np.delete(all_rates_to_normalize_by, participant_id, axis=0)
    
    return rate_to_normalize, rates_to_normalize_by

def get_normalized_rate(rate_to_normalize, rates_to_normalize_by):
    normalized_rate = rate_to_normalize / np.mean(rates_to_normalize_by, axis=0)
    
    return normalized_rate 

def get_latency(min_value_list, rate_list, scale):
    index_list = []
    for idx, val in enumerate(min_value_list):
        minimum_index = np.where(rate_list[idx] == val)[0][0]
        index_list.append(scale[minimum_index])
    return index_list






