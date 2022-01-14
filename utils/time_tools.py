#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time    : 2021/12/9 9:25
# @File : time_tools.py 
# @Author  : 黄权权
# @Software: PyCharm
# @Desc    : None
import datetime
import time


def get_timeString(time_formate="%Y-%m-%d %H:%M:%S", yesterday=False, tomorrow=False):
    """
    获取时间字符串
    :param time_formate: 时间字符串的格式
    :param yesterday: 获取前一天的时间
    :param tomorrow: 获取后一天的时间
    :return:
    """
    # 获取当前时间
    current_time = datetime.datetime.now()
    if yesterday:
        # 用今天时间减1，就是昨天的时间
        yesterday_time = current_time - datetime.timedelta(days=1)
        time_string = yesterday_time.strftime(time_formate)
    elif tomorrow:
        # 用今天时间加1，就是明天的时间
        tomorrow_time = current_time + datetime.timedelta(days=1)
        time_string = tomorrow_time.strftime(time_formate)
    else:
        time_string = current_time.strftime(time_formate)
    return time_string

# 获取距离现在时间的任意时间的日期
def getAnyDateTime(time_formate="%Y-%m-%d %H:%M:%S", day=0, hour=0, min=0, sec=0):
    """
    获取距离现在时间的任意时间的日期&时间
    time_formate:   时间格式
    day:          天数 1代表当前时间+1天    -1代表当前时间-1天     默认=0
    hour:         小时 2代表当前时间+2h     -2代表当前时间-2h     默认=0
    min:          分钟 30代表当前时间+30min -30代表当前时间-30m   默认=0
    sec:          秒   120代表当前时间+120s -120代表当前时间-120s 默认=0
    return:       2019-05-15 15:37:41 -> str
    """
    # 获取当前时间
    current_time = datetime.datetime.now()
    # 与当前时间的时间差
    current_time_timedelta = datetime.timedelta(days=day, hours=hour, minutes=min, seconds=sec)
    # 两种时间相加得出日期时间
    time_str = current_time + current_time_timedelta
    # 格式化时间，以字符串返回
    time_string = time_str.strftime(time_formate)
    return time_string

# 获取当前时间-毫秒级
def getCurrentMilliSecondTime():
    """
    获取当前时间-毫秒级
    return:       1557730376981 -> str
    """
    timestamps = str(round(time.time() * 1000))
    return timestamps

# 获取当前时间-秒级
def getCurrentSecondTime():
    """
    获取当前时间-秒级
    :return:
    """
    timeStr = str(round(time.time()))
    return timeStr

if __name__ == '__main__':
    print(getCurrentMilliSecondTime())
