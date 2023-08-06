"""
    
    Module contains tools to deal with the process related to time and scheduling 

    
"""

from enum import Enum
import typing
from typing import Coroutine, Generator
import time, datetime
import asyncio
import re
from calendar import delta_time_from_now


class Schedule:
    def __init__(self):
        self.tasks = []

    async def __to_do_after(self, fnc, delay):
        await asyncio.sleep(delay)
        await fnc

    def add_event(self, task, hour, date=None, name=None):
        delay = delta_time_from_now(hour, date)
        self.tasks.append(self.__to_do_after(task, delay))

    def start(self):
        async def main():
            concurrent_tasks = []
            for task in self.tasks:
                concurrent_tasks.append(asyncio.create_task(task))
            for task in concurrent_tasks:
                await task

        asyncio.run(main())
