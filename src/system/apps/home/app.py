# VxOS
# 
# Copyright (C) Voxellius Systems. All Rights Reserved.
# Please refer to LICENCE.md for licensing information.
# 
# https://voxellius.com

import vx.app as app
import vx.gui as gui

class HomeProcess(app.Process):
    async def run(self):
        app.startApp("system/apps/statusbar")

        await app.defer()

        screen = gui.ScrollableScreen()
        screen.name = "Home"

        gui.screenContainer.add(screen)
        gui.switchToScreen(screen)

        await app.defer()

        tileContainer = gui.Container(0, 0, None, 96)

        screen.contents.add(tileContainer)

        await app.defer()

        previousTile = None

        def onTileFocus(event):
            if event.target.computedX + event.target.computedWidth > tileContainer.computedWidth:
                tileContainer.x = -event.target.x + (tileContainer.computedWidth - event.target.computedWidth - (2 * event.target.xMargin))

            if event.target.computedX < 0:
                tileContainer.x = -event.target.x

        for i in range(0, 4):
            tile = gui.Button(0, 0, "Tile {}".format(i), 176, None, 8, 8)

            tile.on(gui.FocusEvent, onTileFocus)

            if previousTile != None:
                tile.place(previousTile, gui.sides.AFTER)
            else:
                tile.focus()

            tileContainer.add(tile)

            await app.defer()

            previousTile = tile

        await app.defer()

        appGrid = gui.Container(0, 0, screen.contents.computedWidth, 10, 8, 0)

        screen.contents.add(appGrid)

        appGrid.place(tileContainer, gui.sides.BELOW)

        await app.defer()

        buttonWidth = appGrid.computedWidth // 4

        for i in range(0, 12):
            button = gui.Button(
                buttonWidth * (i % 4),
                64 * (i // 4),
                "App {}".format(i),
                buttonWidth,
                64
            )

            button.holdRender()

            button.borderThickness = 0

            appGrid.add(button)
            button.releaseRender()

            await app.defer()

        appGrid.height = appGrid.contentsHeight

        screen.render()

        while True:
            screen.updateFocusPosition()

            await app.defer()

process = HomeProcess