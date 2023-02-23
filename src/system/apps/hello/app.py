# VxOS
# 
# Copyright (C) Voxellius Systems. All Rights Reserved.
# Please refer to LICENCE.md for licensing information.
# 
# https://voxellius.com

import vx.app
import vx.gui as gui
import vx.platform
import vx.display
import vx.keyboard
import vx.time

class HelloProcess(vx.app.Process):
    async def run(self):
        vx.app.startApp("system/apps/statusbar")

        screen = vx.gui.Screen()

        gui.screenContainer.add(screen)

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

        button3 = gui.Button(260, 50, ":D", 50)

        screen.add(button3)

        await vx.app.defer()

        clock = gui.Text(2, 154, "00:00:00", gui.fonts.SANS_NUMERALS_64)

        screen.add(clock)

        await vx.app.defer()

        counter = gui.Text(10, 214, "")
        i = 0

        screen.add(counter)

        await vx.app.defer()

        button.focus()

        print(vx.gui.getElements(lambda element: element.focusable))

        await vx.app.defer()

        while True:
            vx.gui.updateEvents()

            keys = vx.keyboard.heldKeys

            clock.text = vx.time.getTimeString(vx.time.TimeFormat(vx.time.timeFormatModes.TIME | vx.time.timeFormatModes.TIME_SECONDS))
            counter.text = str(keys) if keys else "No events"

            i += 1

            await vx.app.defer()

process = HelloProcess