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

font = bitmap_font.load_font("assets/titilliumweb-regular-16.bdf")

label = Label(font = font, text = "Hello, world!", x = 20, y = 0, scale = 1, color = 0x000000)

box = gui.Box(0, 0, None, 20)

vx.display.rootGroup.append(label)

gui.rootContainer.add(box)

while True:
    label.y += 1

    if label.y > 200:
        label.y = 0

    time.sleep(0.001)