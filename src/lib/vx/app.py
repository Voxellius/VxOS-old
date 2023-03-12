# VxOS
# 
# Copyright (C) Voxellius Systems. All Rights Reserved.
# Please refer to LICENCE.md for licensing information.
# 
# https://voxellius.com

import asyncio

import vx.gui

runningProcesses = []

class Process:
    def __init__(self, arguments):
        self.arguments = arguments

        self.path = None
        self.task = None

    async def run(self):
        pass

class ScreenStackProcess(Process):
    def __init__(self, arguments):
        super().__init__(arguments)

        self.screenStack = []

    async def start(self):
        pass

    async def registerScreen(self, screen):
        if screen.isRegistered:
            return screen

        screen.process = self
        screen.isRegistered = True

        vx.gui.screenContainer.add(screen)

        await screen._start()

        return screen

    async def openScreen(self, screen):
        await self.registerScreen(screen)

        self.screenStack.append(screen)

        vx.gui.switchToScreen(screen)

    async def closeScreen(self, screen = None):
        if screen == None:
            screen = self.screenStack[-1]

        self.screenStack.remove(screen)

        if len(self.screenStack) > 0:
            vx.gui.switchToScreen(self.screenStack[-1])

    async def run(self):
        await self.start()
        await self.openScreen(self.startingScreen())

        while len(self.screenStack) > 0:
            await defer()

            shouldLoop = False

            for screen in self.screenStack:
                if screen.visible:
                    shouldLoop = True

            if shouldLoop:
                await self.screenStack[-1]._loop()

        vx.gui.goHome()

async def defer():
    await asyncio.sleep(0)

def startAsync(functionCall):
    asyncio.create_task(functionCall)

def startProcess(processClass, arguments = {}):
    process = processClass(arguments)
    process.task = asyncio.create_task(process.run())

    runningProcesses.append(process)

    return process

def startApp(path):
    app = __import__(path.replace("/", ".") + ".app", None, None, [None])

    app.process.path = path

    return startProcess(app.process)