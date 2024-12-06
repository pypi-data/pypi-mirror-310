#!/usr/bin/env python
# -*- coding:utf-8 -*-
from datetime import time, datetime, date
from typing import Union

__all__ = []

TimeType = Union[tuple[int, int, int], time, datetime]
DateType = Union[tuple[int, int, int], date, datetime]
DateTimeType = Union[tuple[int, int, int, int, int, int], str, datetime]


def _handle_time_type(origin) -> time:
    if isinstance(origin, time):
        return origin
    elif isinstance(origin, datetime):
        return origin.time()
    elif isinstance(origin, tuple):
        if len(origin) < 3:
            raise ValueError(f"TimeType tuple format need 3 values. like: (23, 59, 59)")
        return time(origin[0], origin[1], origin[2])
    else:
        raise TypeError(f"not support type '{type(origin).__name__}'")


def _handle_date_type(origin) -> date:
    if isinstance(origin, date):
        return origin
    elif isinstance(origin, datetime):
        return origin.date()
    elif isinstance(origin, tuple):
        if len(origin) < 3:
            raise ValueError(f"DateType tuple format need 3 values. like: (1970, 1, 1)")
        return date(origin[0], origin[1], origin[2])
    else:
        raise TypeError(f"not support type '{type(origin).__name__}'")


def _handle_datetime_type(origin, str_format: str = None) -> datetime:
    if isinstance(origin, datetime):
        return origin
    elif isinstance(origin, tuple):
        if len(origin) < 6:
            raise ValueError(f"TimeType tuple format need 3 values. like: (1970, 1, 1, 23, 59, 59)")
        return datetime(origin[0], origin[1], origin[2], origin[3], origin[4], origin[5])
    elif isinstance(origin, str):
        return datetime.strptime(origin, str_format or "%Y-%m-%d %H:%M:%S")
    else:
        raise TypeError(f"not support type '{type(origin).__name__}'")

