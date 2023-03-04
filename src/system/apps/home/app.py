# VxOS
# 
# Copyright (C) Voxellius Systems. All Rights Reserved.
# Please refer to LICENCE.md for licensing information.
# 
# https://voxellius.com

import vx.app as app
import vx.gui as gui
import vx.platform as platform
import vx.display as display

class AppButton(gui.FocusableBox):
    def __init__(self, x, y, appName, appIcon, width = 128, height = 96, xMargin = 0, yMargin = 0):
        self.appName = appName
        self.appIcon = appIcon

        self.appNameText = gui.Text(0, 8, appName)
        self.appNameText._foreground = display.BLACK

        self.appIconImage = gui.Image(0, 8, appIcon)

        super().__init__(x, y, width, height, xMargin, yMargin)

        self.add(self.appNameText, False)
        self.add(self.appIconImage, False)

    def _updateBuild(self):
        super()._updateBuild()

        self.appNameText.render() # This is so we can find the computed width for centering the text
        self.appNameText.holdRender()

        if self.focused:
            self.appNameText.foreground = display.WHITE
        else:
            self.appNameText.foreground = display.BLACK

        if self.parent != None:
            self.appNameText.text = self.appName

            self.appNameText.x = (self.computedWidth - self.appNameText.computedWidth) // 2
            self.appNameText.y = self.computedHeight - self.appNameText.computedHeight - 8

            self.appIconImage.align(gui.alignments.MIDDLE, gui.alignments.START)

        self.appNameText.releaseRender()

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

            previousTile = tile

        await app.defer()

        appGrid = gui.Container(0, 0, screen.contents.computedWidth, 10, 8, 0)

        screen.contents.add(appGrid)

        appGrid.place(tileContainer, gui.sides.BELOW)

        await app.defer()

        buttonWidth = appGrid.computedWidth // 4

        for i in range(0, 8):
            button = AppButton(
                buttonWidth * (i % 4),
                96 * (i // 4),
                "App {}".format(i),
                "assets/appicon.bmp",
                buttonWidth
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

            tileContainer.children[0].text = platform.memoryFree

            await app.defer()

process = HomeProcess