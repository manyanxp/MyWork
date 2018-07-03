# -*- utf-8 -*-
import io
import time
import threading
import asyncio
from threading import Lock
from concurrent.futures import ThreadPoolExecutor
   
class Event():
    __pool = ThreadPoolExecutor(max_workers = 128)
    def __init__(self):
        self.event = None

    def handler(self, *args, **keyags):
        """スレッドプール起動"""
        try:
            if self.event is not None:
                self.__pool.submit(self.event(args, keyags))
        except:
            print("異常")

    def run(self):
       self.handler([1,1])

def func(*args, **keyags):
    print("test")

if __name__ == '__main__':
    e = Event()
    e.event = func
    e.run()

    pass