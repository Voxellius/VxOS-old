# VxOS
# 
# Copyright (C) Voxellius Systems. All Rights Reserved.
# Please refer to LICENCE.md for licensing information.
# 
# https://voxellius.com

import vx.platform
import vx.display
import vx.gui as gui

import gc
import time

box = gui.Box(0, 0, None, 20)

gui.rootContainer.add(box)

vx.display.display.refresh()
vx.display.display.refresh()

vx.display.display.auto_refresh = False

button = gui.Button(20, 50, "Hello")

gui.rootContainer.add(button)

button2 = gui.Button(140, 50, "world")

gui.rootContainer.add(button2)

clock = gui.Text(2, 160, "12:34", gui.fonts.SANS_NUMERALS_64)

gui.rootContainer.add(clock)

counter = gui.Text(10, 220, "")
i = 0

gui.rootContainer.add(counter)

vx.display.display.refresh()
vx.display.display.refresh()

if vx.platform.IS_REAL_HARDWARE:
    vx.display.display.auto_refresh = True

time.sleep(2)

vx.display.display.auto_refresh = False

button.focus()

while True:
    if vx.platform.IS_REAL_HARDWARE and i % 10 == 0:
        clock.text = str(gc.mem_free())

    counter.text = str(i)

    vx.display.display.refresh()
    vx.display.display.refresh()

    i += 1

    gc.collect()

    time.sleep(0.001)