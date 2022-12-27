# VxOS
# 
# Copyright (C) Voxellius Systems. All Rights Reserved.
# Please refer to LICENCE.md for licensing information.
# 
# https://voxellius.com

import displayio

import vx.platform

displayio.release_displays()

WIDTH = 400
HEIGHT = 240

if vx.platform.IS_REAL_HARDWARE:
    import busio
    import board
    import sharpdisplay
    import framebufferio

    bus = busio.SPI(board.SCK, MOSI = board.MOSI)

    framebuffer = sharpdisplay.SharpMemoryFramebuffer(bus, board.D6, WIDTH, HEIGHT)
    display = framebufferio.FramebufferDisplay(framebuffer) 
else:
    import blinka_displayio_pygamedisplay

    display = blinka_displayio_pygamedisplay.PyGameDisplay(width = WIDTH, height = HEIGHT)

print(vx.platform.IS_REAL_HARDWARE)