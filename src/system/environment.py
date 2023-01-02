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

async def init(initAppPath):
    vx.gui._getFont("titilliumweb-regular-16")
    vx.gui._getFont("titilliumweb-numerals-64")

    vx.platform.update()

    vx.display.display.auto_refresh = False

    vx.app.startApp(initAppPath)

    i = 0

    while True:
        gc.collect()

        vx.display.display.refresh()
        vx.display.display.refresh()

        if i % 100 == 0:
            gc.collect()

            vx.platform.update()

        i += 1

        await vx.app.defer()