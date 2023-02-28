# VxOS
# 
# Copyright (C) Voxellius Systems. All Rights Reserved.
# Please refer to LICENCE.md for licensing information.
# 
# https://voxellius.com

import adafruit_platformdetect

_platformDetector = adafruit_platformdetect.Detector()

IS_REAL_HARDWARE = not _platformDetector.board.generic_linux

class batteryStates:
    UNKNOWN = 0
    DISCHARGING = 1
    CHARGING = 2

currentBatteryLevel = 0
currentBatteryState = batteryStates.UNKNOWN
memoryFree = 0

def update():
    global currentBatteryLevel, memoryFree

    if IS_REAL_HARDWARE:
        currentBatteryLevel = sensor.cell_percent

        memoryFree = gc.mem_free()

if IS_REAL_HARDWARE:
    import board
    import gc
    from adafruit_lc709203f import LC709203F, PackSize

    sensor = LC709203F(board.I2C())
    sensor.pack_size = PackSize.MAH3000