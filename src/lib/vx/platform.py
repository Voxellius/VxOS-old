# VxOS
# 
# Copyright (C) Voxellius Systems. All Rights Reserved.
# Please refer to LICENCE.md for licensing information.
# 
# https://voxellius.com

import adafruit_platformdetect

_platformDetector = adafruit_platformdetect.Detector()

IS_REAL_HARDWARE = not _platformDetector.board.generic_linux

_MIN_BATTERY_VOLTAGE = 3
_MAX_BATTERY_VOLTAGE = 4

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
        _batteryVoltage = batteryVoltageSensor.value / 5371
        currentBatteryLevel = min(max((_batteryVoltage - _MIN_BATTERY_VOLTAGE) / (_MAX_BATTERY_VOLTAGE - _MIN_BATTERY_VOLTAGE), 0), 1) * 100

        memoryFree = gc.mem_free()

if IS_REAL_HARDWARE:
    import board
    import gc
    import analogio
    import digitalio

    batteryVoltageSensor = analogio.AnalogIn(board.BATTERY)

    batteryChargingSensor = digitalio.DigitalInOut(board.VBUS_SENSE)
    batteryChargingSensor.direction = digitalio.Direction.INPUT