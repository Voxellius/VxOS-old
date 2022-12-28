# VxOS
# 
# Copyright (C) Voxellius Systems. All Rights Reserved.
# Please refer to LICENCE.md for licensing information.
# 
# https://voxellius.com

import vx.gui as gui

import time

box = gui.Box(0, 0, None, 20)

gui.rootContainer.add(box)

button = gui.Button(20, 50, "Hi")

gui.rootContainer.add(button)

clock = gui.Text(2, 160, "12:34", gui.fonts.SANS_NUMERALS_64)

gui.rootContainer.add(clock)

time.sleep(2)

button.focus()

while True:
    time.sleep(0.001)