# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import datetime
import time


class Stopwatch(object):

    def __init__(self):
        self.__is_run = False
        self.__start_time = 0
        self.__elapsed_times = 0

    def start(self):
        if self.__is_run:
            return False
        self.__is_run = True
        self.__start_time = time.time()

    def stop(self):
        if not self.__is_run:
            return False
        self.__is_run = False
        self.__elapsed_times += time.time() - self.__start_time

    def elapsed(self):

        if self.__is_run:
            return self.__elapsed_times + time.time() - self.__start_time
        return self.__elapsed_times

    def reset(self):

        self.__elapsed_times = 0
        self.__start_time = 0


def timestamp_to_date(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp)


def http_to_unixtime(time_string):
    """把HTTP Date格式的字符串转换为UNIX时间（自1970年1月1日UTC零点的秒数）。

    HTTP Date形如 `Sat, 05 Dec 2015 11:10:29 GMT` 。
    """
    tm = time.mktime(time.strptime(time_string, '%a, %d %b %Y %H:%M:%S  GMT'))
    return tm
