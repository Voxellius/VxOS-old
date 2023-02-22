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

        def buttonKeyEvent(event):
            button.text = event.key.name

        button.on(gui.KeyPressEvent, buttonKeyEvent)

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
            vx.gui.updateEvents()

            keys = vx.keyboard.heldKeys

            clock.text = vx.time.getTimeString(vx.time.TimeFormat(False, True, True))
            date.text = "%s (%.1f%% battery)" % (
                vx.time.getTimeString(vx.time.TimeFormat(True, False, False)),
                vx.platform.currentBatteryLevel
            )

            counter.text = str(keys) if keys else "No events"

            i += 1

            await vx.app.defer()

process = HelloProcess