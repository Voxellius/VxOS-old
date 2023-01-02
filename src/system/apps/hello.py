# VxOS
# 
# Copyright (C) Voxellius Systems. All Rights Reserved.
# Please refer to LICENCE.md for licensing information.
# 
# https://voxellius.com

import vx.platform
import vx.display
import vx.keyboard
import vx.app
import vx.gui as gui

class HelloProcess(vx.app.Process):
    async def run(self):
        screen = vx.gui.Screen()

        gui.rootContainer.add(screen)

        gui.switchToScreen(screen)

        await vx.app.defer()

        button = gui.Button(20, 50, "Hello")

        screen.add(button)

        await vx.app.defer()

        button2 = gui.Button(140, 50, "world")

        screen.add(button2)

        await vx.app.defer()

        clock = gui.Text(2, 160, "12:34", gui.fonts.SANS_NUMERALS_64)

        screen.add(clock)

        await vx.app.defer()

        counter = gui.Text(10, 220, "")
        i = 0

        screen.add(counter)

        await vx.app.defer()

        button.focus()

        print(vx.gui.getElements(lambda element: element.focusable))

        await vx.app.defer()

        while True:
            keys = vx.keyboard.poll()

            if keys:
                counter.text = str(keys)
            else:
                counter.text = "(%d) No events (%.1f%% battery)" % (i, vx.platform.currentBatteryLevel)

            i += 1

            await vx.app.defer()

process = HelloProcess