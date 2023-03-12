# VxOS
# 
# Copyright (C) Voxellius Systems. All Rights Reserved.
# Please refer to LICENCE.md for licensing information.
# 
# https://voxellius.com

import vx.app as app
import vx.gui as gui
import vx.platform
import vx.display
import vx.keyboard
import vx.time

class HelloScreen(gui.ScrollableScreen):
    async def start(self):
        self.name = "Hello, world!"

        await app.defer()

        button = gui.Button(16, 26, "Hello")

        self.contents.add(button)

        def buttonKeyEvent(event):
            button.text = event.key.name

            button.render()

        button.on(gui.KeyPressEvent, buttonKeyEvent)

        await vx.app.defer()

        button2 = gui.Button(16, 26, "world")

        button2.place(button, gui.sides.AFTER, 8)

        self.contents.add(button2)

        await vx.app.defer()

        button3 = gui.Button(260, 230, ":D", 48)

        self.contents.add(button3)

        await vx.app.defer()

        self.clock = gui.Text(16, 114, "00:00:00", gui.fonts.SANS_NUMERALS_64)

        self.contents.add(self.clock)

        await vx.app.defer()

        self.counter = gui.Text(16, 180, "")
        
        self.i = 0

        self.contents.add(self.counter)

        await vx.app.defer()

        button.focus()

        print(vx.gui.getElements(lambda element: element.focusable))

    async def loop(self):
        keys = vx.keyboard.heldKeys

        self.clock.text = vx.time.getTimeString(vx.time.TimeFormat(vx.time.timeFormatModes.TIME | vx.time.timeFormatModes.TIME_SECONDS))
        self.counter.text = str(keys) if keys else "No keys held down ({})".format(self.i)

        self.i += 1

class HelloProcess(app.ScreenStackProcess):
    startingScreen = HelloScreen

process = HelloProcess