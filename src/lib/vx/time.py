# VxOS
# 
# Copyright (C) Voxellius Systems. All Rights Reserved.
# Please refer to LICENCE.md for licensing information.
# 
# https://voxellius.com

import time

import vx.platform

if vx.platform.IS_REAL_HARDWARE:
    from adafruit_datetime import datetime as _datetime, timedelta
else:
    from datetime import datetime as _datetime, timedelta

datetime = _datetime

_initialTimestamp = time.time()
_timeOffset = 0

class TimeFormat:
    def __init__(self, date, time, timeSeconds):
        self.date = date
        self.time = time
        self.timeSeconds = timeSeconds

def now():
    return datetime.now() + timedelta(0, _timeOffset)

def setTime(dt = datetime(2023, 1, 1, 0, 0, 0)):
    global _timeOffset

    if not vx.platform.IS_REAL_HARDWARE:
        return
    
    _timeOffset = time.mktime(dt.timetuple()) - _initialTimestamp

def getTimeString(format = TimeFormat(True, True, False), dt = None):
    if dt == None:
        dt = now()

    fullString = ""

    if format.date:
        fullString += "%02d/%02d/%d" % (dt.day, dt.month, dt.year)

        if format.time:
            fullString += " "

    if format.time:
        fullString += "%02d:%02d" % (dt.hour, dt.minute)

        if format.timeSeconds:
            fullString += ":%02d" % (dt.second)

    return fullString