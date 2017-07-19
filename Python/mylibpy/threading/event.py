# -*- utf-8 -*-
import io
import time
import threading
import asyncio
from threading import Lock
from concurrent.futures import ThreadPoolExecutor

class Event():
    __pool = ThreadPoolExecutor(max_workers = 128)
    event = None
    def __init__(self):
        pass

    def handler(self, **keyags):
        """スレッドプール起動"""
        try:
            if self.event is not None:
                self.__pool.submit(self.event(keyags))
        except:
            print("異常")

          


    