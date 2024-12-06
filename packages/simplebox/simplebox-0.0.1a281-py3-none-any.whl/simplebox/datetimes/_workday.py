#!/usr/bin/env python
# -*- coding:utf-8 -*-

from datetime import datetime, date, time, timedelta
from typing import Optional

from dateutil.rrule import rrule, DAILY

from ._datetype import DateType, DateTimeType, TimeType, _handle_time_type, _handle_date_type, _handle_datetime_type

__all__ = []


class WorkingDay:

    def __init__(self, holidays: tuple[DateType] or None = None):
        if not isinstance(holidays, (tuple, type(None))):
            raise TypeError(f"need a tuple type, got '{type(holidays).__name__}'")

        self.__holidays_of_date: list[DateType] = []
        if holidays is not None:
            for holiday in holidays:
                self.__holidays_of_date.append(_handle_date_type(holiday))

    def is_weekend(self, day):
        """check date is weekend"""
        return day.weekday() >= 5

    def is_holiday(self, day):
        """check date is holiday"""
        return day in self.__holidays_of_date

    def is_working_day(self, day):
        """check date is working day"""
        return not (self.is_weekend(day) or self.is_holiday(day))

    def calculate_working(self, start: DateTimeType, end: DateTimeType, work_start: Optional[TimeType] = None,
                          work_end: Optional[TimeType] = None) -> timedelta:
        start_ = _handle_datetime_type(start)
        end_ = _handle_datetime_type(end)
        if start_ > end_:
            start_, end_ = end_, start

        work_start_ = _handle_time_type(work_start or time(9, 0, 0))
        work_end_ = _handle_time_type(work_end or time(18, 0, 0))

        if datetime.combine(datetime.today(), work_start_) > datetime.combine(datetime.today(), work_end_):
            work_end_, work_start_ = work_start_, work_end_

        end_worK_start_datetime = datetime(end_.year, end_.month, end_.day,
                                           work_start_.hour, work_start_.minute, work_start_.second)
        start_worK_end_datetime = datetime(start_.year, start_.month, start_.day,
                                           work_end_.hour, work_end_.minute, work_end_.second)
        total_seconds = timedelta()
        for dt in rrule(DAILY, dtstart=start_, until=end_):
            dt_date = dt.date()
            if self.is_working_day(dt_date):
                if dt_date == start_.date():
                    print((start_worK_end_datetime - dt).total_seconds())
                    total_seconds += (start_worK_end_datetime - dt)
                elif dt_date == end_.date():
                    print((dt - end_worK_start_datetime).total_seconds())
                    total_seconds += (dt - end_worK_start_datetime)
                else:
                    print((datetime.combine(dt_date, start_worK_end_datetime.time()) -
                           datetime.combine(dt_date, end_worK_start_datetime.time())).total_seconds())
                    total_seconds += (datetime.combine(dt_date, start_worK_end_datetime.time()) -
                                      datetime.combine(dt_date, end_worK_start_datetime.time()))
        return total_seconds
