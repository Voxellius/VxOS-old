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

BLACK = 0x000000
WHITE = 0xFFFFFF

def invertColour(colour):
    return 0xFFFFFF - colour

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

rootGroup = displayio.Group()

backgroundColourShader = displayio.Palette(1)
backgroundColourShader[0] = 0xFFFFFF

backgroundBitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
backgroundGrid = displayio.TileGrid(backgroundBitmap, pixel_shader = backgroundColourShader, x = 0, y = 0)

rootGroup.append(backgroundGrid)

display.show(rootGroup)