# VxOS
# 
# Copyright (C) Voxellius Systems. All Rights Reserved.
# Please refer to LICENCE.md for licensing information.
# 
# https://voxellius.com

import vx.app
import vx.gui as gui
import vx.display
import vx.time

class StatusBarProcess(vx.app.Process):
    async def run(self):
        container = gui.Box(-2, -2, vx.display.WIDTH + 4, 24 + 2)
        timeText = gui.Text(4, 0, "")

        gui.rootContainer.add(container)
        container.add(timeText)

        while True:
            timeText.x = 8
            timeText.text = "%.1f%% - %s" % (
                vx.platform.currentBatteryLevel,
                vx.time.getTimeString(vx.time.TimeFormat(vx.time.timeFormatModes.TIME))
            )

            timeText.align(gui.alignments.END, gui.alignments.MIDDLE)

            await vx.app.defer()

process = StatusBarProcess