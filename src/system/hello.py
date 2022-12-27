# VxOS
# 
# Copyright (C) Voxellius Systems. All Rights Reserved.
# Please refer to LICENCE.md for licensing information.
# 
# https://voxellius.com

import vx.display
import vx.gui as gui

from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font
import time

font = bitmap_font.load_font("assets/titilliumweb-numerals-64.bdf")

box = gui.Box(0, 0, None, 20)

gui.rootContainer.add(box)

label = Label(font = font, text = "0123456789", x = 200, y = 120, scale = 1, color = 0x000000)

vx.display.rootGroup.append(label)

while True:
    label.x -= 1

    if label.x < -400:
        label.x = 400

    time.sleep(0.001)