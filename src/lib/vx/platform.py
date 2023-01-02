# VxOS
# 
# Copyright (C) Voxellius Systems. All Rights Reserved.
# Please refer to LICENCE.md for licensing information.
# 
# https://voxellius.com

import adafruit_platformdetect

_platformDetector = adafruit_platformdetect.Detector()

IS_REAL_HARDWARE = not _platformDetector.board.generic_linux

currentBatteryLevel = 0

def update():
    global currentBatteryLevel

    if IS_REAL_HARDWARE:
        currentBatteryLevel = sensor.cell_percent

if IS_REAL_HARDWARE:
    import board
    from adafruit_lc709203f import LC709203F, PackSize

    sensor = LC709203F(board.I2C())
    sensor.pack_size = PackSize.MAH3000