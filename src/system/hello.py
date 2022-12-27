# VxOS
# 
# Copyright (C) Voxellius Systems. All Rights Reserved.
# Please refer to LICENCE.md for licensing information.
# 
# https://voxellius.com

import vx.display

import terminalio
from adafruit_display_text.label import Label

print("Testing this!")

vx.display.display.show(Label(font = terminalio.FONT, text = "Hello, world!", x = 20, y = 20, scale = 4, color = 0xFFFFFF))

while True: pass