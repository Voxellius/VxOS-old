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
        await vx.app.defer()

        screen = vx.gui.ScrollableScreen()
        screen.name = "Hello, world!"

        gui.screenContainer.add(screen)
        gui.switchToScreen(screen)

        await vx.app.defer()

        button = gui.Button(16, 26, "Hello")

        screen.contents.add(button)

        def buttonKeyEvent(event):
            button.text = event.key.name

        button.on(gui.KeyPressEvent, buttonKeyEvent)

        await vx.app.defer()

        button2 = gui.Button(16, 26, "world")

        button2.place(button, gui.sides.AFTER, 8)

        screen.contents.add(button2)

        await vx.app.defer()

        button3 = gui.Button(260, 230, ":D", 48)

        screen.contents.add(button3)

        await vx.app.defer()

        clock = gui.Text(16, 114, "00:00:00", gui.fonts.SANS_NUMERALS_64)

        screen.contents.add(clock)

        await vx.app.defer()

        counter = gui.Text(16, 180, "")
        i = 0

        screen.contents.add(counter)

        await vx.app.defer()

        button.focus()

        print(vx.gui.getElements(lambda element: element.focusable))

        await vx.app.defer()

        screen.render()

        while True:
            keys = vx.keyboard.heldKeys

            clock.text = vx.time.getTimeString(vx.time.TimeFormat(vx.time.timeFormatModes.TIME | vx.time.timeFormatModes.TIME_SECONDS))
            counter.text = str(keys) if keys else "No keys held down ({})".format(i)

            i += 1

            await vx.app.defer()

process = HelloProcess