# VxOS
# 
# Copyright (C) Voxellius Systems. All Rights Reserved.
# Please refer to LICENCE.md for licensing information.
# 
# https://voxellius.com

import adafruit_platformdetect

platformDetector = adafruit_platformdetect.Detector()

IS_REAL_HARDWARE = not platformDetector.board.generic_linux