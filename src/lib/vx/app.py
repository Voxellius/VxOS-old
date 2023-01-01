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

        self.task = None

    async def run(self):
        pass

def startProcess(processClass, arguments = {}):
    process = processClass(arguments)
    process.task = asyncio.create_task(process.run())

    def endTask(task):
        process.task = None

    process.task.add_done_callback(endTask)

    runningProcesses.push(process)