# -*- utf-8 -*-

#-----------------------------------------------------------------------
# stopwatch.py
#-----------------------------------------------------------------------

import sys
import time

#-----------------------------------------------------------------------
class Stopwatch():
    def __init__(self):
        self.__elapsed_time = 0
        self.__creation_time = 0

    @property
    def elapsed_time(self):
        return self.__elapsed_time

    # 計測開始
    def start(self):
        self.__creation_time = time.time()

    # 計測終了
    def end(self):
        self.__elapsed_time = time.time() - self.__creation_time
        return self.__elapsed_time 

