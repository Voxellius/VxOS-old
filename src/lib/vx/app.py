# VxOS
# 
# Copyright (C) Voxellius Systems. All Rights Reserved.
# Please refer to LICENCE.md for licensing information.
# 
# https://voxellius.com

import asyncio

runningProcesses = []

class Process:
    def __init__(self, arguments):
        self.arguments = arguments

        self.path = None
        self.task = None

    async def run(self):
        pass

async def defer():
    await asyncio.sleep(0)

def startProcess(processClass, arguments = {}):
    process = processClass(arguments)
    process.task = asyncio.create_task(process.run())

    runningProcesses.append(process)

    return process

def startApp(path):
    app = __import__(path.replace("/", ".") + ".app", None, None, [None])

    app.process.path = path

    return startProcess(app.process)