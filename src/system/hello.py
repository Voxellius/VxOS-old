# VxOS
# 
# Copyright (C) Voxellius Systems. All Rights Reserved.
# Please refer to LICENCE.md for licensing information.
# 
# https://voxellius.com

import vx.display

from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font
import time

font = bitmap_font.load_font("assets/titilliumweb-regular-16.bdf")

label = Label(font = font, text = "Hello, world!", x = 20, y = 20, scale = 1, color = 0x000000)

vx.display.rootGroup.append(label)

# vx.display.display.show(vx.display.rootGroup)

while True:
    label.y += 1

    if label.y > 200:
        label.y = 20

    time.sleep(0.001)