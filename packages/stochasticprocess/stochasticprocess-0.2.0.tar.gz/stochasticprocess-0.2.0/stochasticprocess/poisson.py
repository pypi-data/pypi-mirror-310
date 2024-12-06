import numpy as np
from math import exp, factorial

def get_event_times(rate=1.0, event_count=1, max_time=None):
    """ Generate event times for a Poisson process up to a specified maximum time or until a certain number of events occur.
    
    Parameters
    ----
    rate: The rate parameter (lambda) of the Poisson process.
    event_count: The number of events to generate.
    max_time: The maximum time up to which events are generated. If None, events are generated until `event_count` is reached.

    Results
    -------
    event_times: A list of event times.
    """
    event_times = []
    t = 0
    while (max_time is None or t < max_time) and len(event_times) < event_count:
        inter_event_time = np.random.exponential(1 / rate)
        t += inter_event_time
        if max_time is None or t < max_time:
            event_times.append(t)
    return event_times

def get_probability(rate=1.0, event_count=0, max_time=1.0):
    """ Calculate the probability of observing exactly `event_count` events in a given time interval.

    Parameters
    ----
    rate: The rate parameter (lambda) of the Poisson process.
    max_time: The time interval.
    event_count: The number of events.

    Results
    ----
    probability: The probability of observing exactly `event_count` events in the given time interval.
    """
    lambda_t = rate * max_time
    probability = (lambda_t ** event_count) * exp(-lambda_t) / factorial(event_count)
    return probability
