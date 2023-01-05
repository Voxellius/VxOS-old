# VxOS
# 
# Copyright (C) Voxellius Systems. All Rights Reserved.
# Please refer to LICENCE.md for licensing information.
# 
# https://voxellius.com

import vx.platform
import vx.display
import vx.keyboard
import vx.time
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

        clock = gui.Text(2, 160, "00:00:00", gui.fonts.SANS_NUMERALS_64)
        date = gui.Text(10, 10, "--/--/----")

        screen.add(clock)
        screen.add(date)

        await vx.app.defer()

        counter = gui.Text(10, 220, "")
        i = 0

        screen.add(counter)

        await vx.app.defer()

        button.focus()

        print(vx.gui.getElements(lambda element: element.focusable))

        await vx.app.defer()

        while True:
            events = vx.gui.getEvents()
            keys = vx.keyboard.poll()

            clock.text = vx.time.getTimeString(vx.time.TimeFormat(False, True, True))
            date.text = vx.time.getTimeString(vx.time.TimeFormat(True, False, False))

            if keys:
                counter.text = str(keys)
            else:
                counter.text = "No events (%.1f%% battery)" % (vx.platform.currentBatteryLevel)

            i += 1

            await vx.app.defer()

process = HelloProcess