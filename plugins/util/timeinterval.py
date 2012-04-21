"""Determines and formats time intervals.

The timestamps provided must seconds since an epoch, such as the ones given
by time.time().
The time intervals are formatted to a maximum of two consecutive units which
span from years to seconds.

"""

import time


time_units = (("year", 60 * 60 * 24 * 365), ("month", 60 * 60 * 24 * 30),
              ("day", 60 * 60 * 24), ("hour", 60 * 60), ("minute", 60),
              ("second", 1))

def format(seconds):
    """Formats a time interval to a maximum of two consecutive units."""
    seconds = abs(seconds)
    b = []
    for i, (name, duration) in enumerate(time_units):
        unit, seconds = divmod(seconds, duration)
        if unit or (seconds == 0 and duration == 1):
            b.append("%d %s%s" % (unit, name, ("s" if unit > 1 else "")))
        if len(b) == 2:
            break
    return ", ".join(b)

def time_since(then, now=None):
    """Determines and formats the time interval between then and now.

    If now is not provided, time.time() will be used.
    If then is after now, it will return '0 second'.
    """
    if now is None:
        now = time.time()
    interval = int(now) - int(then) if int(now) > int(then) else 0
    return format(interval)

def time_until(then, now=None):
    """Determines and formats the time interval between now and then.

    If now is not provided, time.time() will be used.
    If then is before now, it will return '0 second'.
    """
    if now is None:
        now = time.time()
    interval = int(then) - int(now) if int(then) > int(now) else 0
    return format(interval)

def time_interval(time1, time2):
    """Determines and formats the time interval between two times."""
    interval = int(time1) - int(time2)
    return format(interval)
