# VxOS
# 
# Copyright (C) Voxellius Systems. All Rights Reserved.
# Please refer to LICENCE.md for licensing information.
# 
# https://voxellius.com

import vx.app as app
import vx.gui as gui
import vx.display
import vx.time

class StatusBarProcess(app.Process):
    async def run(self):
        container = gui.Box(-2, -2, vx.display.WIDTH + 4, 24 + 2)

        gui.statusBar = container

        screenNameText = gui.Text(8, 0, "")
        timeText = gui.Text(0, 0, "")
        batteryImage = gui.Image(0, 0, "assets/battery-0.bmp")

        lastScreenName = None
        lastTimeString = None
        lastBatteryImageLevel = None

        container.add(screenNameText)
        container.add(timeText)
        container.add(batteryImage)

        await app.defer()

        gui.rootContainer.add(container)

        while True:
            changesMade = False

            currentScreen = gui.getCurrentScreen()
            screenName = currentScreen.name if currentScreen != None else ""

            if screenName != lastScreenName:
                screenNameText.text = screenName

                screenNameText.align(gui.alignments.START, gui.alignments.MIDDLE)

                lastScreenName = screenName
                changesMade = True

            timeString = vx.time.getTimeString(vx.time.TimeFormat(vx.time.timeFormatModes.TIME))

            if timeString != lastTimeString:
                timeText.x = 8
                timeText.text = timeString

                timeText.align(gui.alignments.END, gui.alignments.MIDDLE)

                lastTimeString = timeString
                changesMade = True

            batteryLevel = round(vx.platform.currentBatteryLevel / 10)

            if lastBatteryImageLevel != batteryLevel:
                container.remove(batteryImage)

                batteryImage = gui.Image(0, 0, "assets/battery-{}.bmp".format(batteryLevel))

                container.add(batteryImage)

                batteryImage.place(timeText, gui.sides.BEFORE, 8)
                batteryImage.align(gui.alignments.START, gui.alignments.MIDDLE)

                lastBatteryImageLevel = batteryLevel
                changesMade = True

            if changesMade:
                screenNameText.cut(batteryImage.x - 8 - screenNameText.x)

            await vx.app.defer()

process = StatusBarProcess