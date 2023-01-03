# VxOS
# 
# Copyright (C) Voxellius Systems. All Rights Reserved.
# Please refer to LICENCE.md for licensing information.
# 
# https://voxellius.com

import os
import sys
import asyncio
import adafruit_platformdetect

platformDetector = adafruit_platformdetect.Detector()

if not platformDetector.board.generic_linux:
    sys.path.append("/system")
else:
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    sys.path.append("./lib")
    sys.path.append("./system")

import vx.time
import system.environment

vx.time.setTime()

asyncio.run(system.environment.init("system.apps.hello"))