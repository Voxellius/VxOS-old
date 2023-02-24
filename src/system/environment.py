# VxOS
# 
# Copyright (C) Voxellius Systems. All Rights Reserved.
# Please refer to LICENCE.md for licensing information.
# 
# https://voxellius.com

import gc
import asyncio

import vx.platform
import vx.display
import vx.keyboard
import vx.app
import vx.gui as gui

bootScreen = gui.Screen()

bootImage = gui.Image(0, 0, "assets/boot.bmp")

bootScreen.add(bootImage)

bootImage.x = int((bootScreen.computedWidth - bootImage.computedWidth) / 2)
bootImage.y = int((bootScreen.computedHeight - bootImage.computedHeight) / 2)

gui.rootContainer.add(bootScreen)

bootScreen.visible = True

async def init(initAppPath):
    vx.gui._getFont("titilliumweb-regular-16")
    vx.gui._getFont("titilliumweb-numerals-64")

    vx.platform.update()

    vx.display.display.auto_refresh = False

    bootScreen.visible = False

    vx.app.startApp(initAppPath)

    i = 0

    while True:
        try:
            vx.display.display.refresh()
            vx.display.display.refresh()
        except:
            print("Too long without deferring")

            raise NotImplementedError("No deferral error handling implemented yet")

        if i % 100 == 0:
            gc.collect()

            vx.platform.update()

        i += 1

        await vx.app.defer()