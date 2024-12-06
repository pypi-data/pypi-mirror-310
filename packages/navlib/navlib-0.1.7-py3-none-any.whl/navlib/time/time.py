"""
CoMPAS Navlib - Time Module

This module provides functions for working with time.

Functions:
    time_now: Returns the current time in microseconds since the epoch in local time.
    time_now_utc: Returns the current time in microseconds since the epoch in UTC.
    utime2datestr: Converts a Unix timestamp to a date string.
    datestr2utime: Converts a date string to a Unix timestamp.

Authors: Sebastián Rodríguez-Martínez and Giancarlo Troni
Contact: srodriguez@mbari.org
Last Update: 2024-03-26
"""

__all__ = [
    "time_now",
    "time_now_utc",
    "utime2datestr",
    "datestr2utime",
]

import datetime

# TODO: Add nav_ti
# def nav_ti(utime: Union[List[float], np.ndarray], t0: float, tn: float) -> Union[List[float], np.ndarray]:
#     """
#     Given a set of timestamps return the range of index that is between t0 and tn.

#     Source: Giancarlo Troni's navlib library.

#     Parameters
#     ----------
#     utime : List[float] | np.ndarray
#         Non saturated values as a list of floats or as a numpy array.
#     t0 : float
#         Lower boundary as a float.
#     tn : float
#     Upper boundary as a float.

#     Returns
#     -------
#     utime_sat : List[float] | np.ndarray
#         Index range between t0 and tn.
#     """
#     idx1 = (utime >= sat(t0, utime[0], utime[-1])).argmax()
#     idx2 = (utime[::-1] <= sat(tn, utime[0], utime[-1]) ).argmax()

#     return np.arange(idx1,len(utime)-idx2)


def time_now() -> float:
    """
    Returns the current time in microseconds since the epoch in local time.

    Returns:
        float: Current time in microseconds since the epoch.

    Example:
        >>> time_now()
        1590678950000000.0
    """
    t = datetime.datetime.now()
    time_received = t.timestamp() * 1.00e6
    return time_received


def time_now_utc() -> float:
    """
    Returns the current time in microseconds since the epoch in UTC.

    Returns:
        float: Current time in microseconds since the epoch.

    Example:
        >>> time_now_utc()
        1590678950000000.0
    """
    t = datetime.datetime.now(datetime.timezone.utc)
    time_received = t.timestamp() * 1.00e6
    return time_received


def utime2datestr(utime: float, datefmt: str = "%Y/%m/%d %H:%M:%S") -> str:
    """
    Converts a Unix timestamp to a date string.

    Args:
        utime (float): Unix timestamp.
        datefmt (str, optional): Date format. Defaults to "%Y/%m/%d %H:%M:%S".

    Returns:
        str: Date string.

    Example:
        >>> utime2datestr(1590678950000000.0)
        '2020/05/28 12:09:10'
    """
    t = datetime.datetime.fromtimestamp(utime / 1.00e6, tz=datetime.timezone.utc)
    return t.strftime(datefmt)


def datestr2utime(datestr: str, datefmt: str = "%Y/%m/%d %H:%M:%S") -> float:
    """
    Converts a date string to a Unix timestamp.

    Args:
        datestr (str): Date string.
        datefmt (str, optional): Date format. Defaults to "%Y/%m/%d %H:%M:%S".

    Returns:
        float: Unix timestamp.

    Example:
        >>> datestr2utime("2020/05/28 12:09:10")
        1590678950000000.0
    """
    t = datetime.datetime.strptime(datestr, datefmt)
    # Force the timezone to UTC
    t = t.replace(tzinfo=datetime.timezone.utc)
    return t.timestamp() * 1.00e6
