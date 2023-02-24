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

        screenNameText = gui.Text(8, 0, "")
        timeText = gui.Text(0, 0, "")
        batteryText = gui.Text(0, 0, "")

        container.add(screenNameText)
        container.add(timeText)
        container.add(batteryText)

        await app.defer()

        gui.rootContainer.add(container)

        while True:
            screenNameText.text = "Hello, world!"

            screenNameText.align(gui.alignments.START, gui.alignments.MIDDLE)

            timeText.x = 8
            timeText.text = vx.time.getTimeString(vx.time.TimeFormat(vx.time.timeFormatModes.TIME))

            timeText.align(gui.alignments.END, gui.alignments.MIDDLE)

            batteryText.text = "%.1f%% battery" % (vx.platform.currentBatteryLevel)

            batteryText.place(timeText, gui.sides.BEFORE, 8)
            batteryText.align(gui.alignments.START, gui.alignments.MIDDLE)

            await vx.app.defer()

process = StatusBarProcess