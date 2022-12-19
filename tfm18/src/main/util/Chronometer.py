from datetime import datetime, timedelta
from typing import Optional

from tfm18.src.main.util.StrUtil import format_time_delta


class Chronometer:
    __start_date_time: datetime
    __time_delta: Optional[timedelta]

    def __init__(self, time_delta: Optional[timedelta] = None):
        self.__start_date_time = datetime.now()
        self.__time_delta = time_delta

    def stop(self) -> timedelta:
        if not self.is_stopped():
            end_date_time: datetime = datetime.now()
            self.__time_delta = end_date_time - self.__start_date_time
        return self.__time_delta

    def __add__(self, other):
        if isinstance(other, Chronometer):
            if not self.is_stopped() or not other.is_stopped():
                raise Exception("Cannot add time to a non stopped Chronometer instance!")
            return Chronometer(time_delta=self.__time_delta + other.__time_delta)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Chronometer):
            if not self.is_stopped() or not other.is_stopped():
                raise Exception("Cannot subtract time to a non stopped Chronometer instance!")
            return Chronometer(time_delta=self.__time_delta - other.__time_delta)
        return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, Chronometer):
            if not self.is_stopped() or not other.is_stopped():
                raise Exception("Cannot add time to a non stopped Chronometer instance!")
            return Chronometer(time_delta=other.__time_delta - self.__time_delta)
        return NotImplemented

    def is_stopped(self) -> bool:
        return self.__time_delta is not None

    def get_elapsed_str(self) -> str:
        self.stop()
        return format_time_delta(self.__time_delta)

    def get_elapsed_millis(self) -> float:
        self.stop()
        return self.__time_delta.total_seconds() * 1000
