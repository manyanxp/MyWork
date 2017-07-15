#-*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
import sys, os
print("[*]Append library path: " 
+ os.path.dirname(os.path.abspath(__file__)) + '/../../Python')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../Python')
#-----------------------------------------------------------------------------

import io
import socket
import time
import threading
from actions import data_controller as dc

# アプリケーションメイン
class App:
    _instance = None
    def __init__(self):
        """アプリケーションの初期化処理"""

        print('[*]Begin... Initalize application')
        self._initalize_resource()
        self._data_controller = dc.DataController()

    @classmethod
    def get_instance(cls):
       """唯一のインスタンスを返す"""
       if cls._instance is None:
            cls._instance = cls()
            return cls._instance

    def _initalize_resource(self):
        """何かｱﾌﾟﾘの初期化処理があれば記述"""
        pass

	# 実行部
    def run(self):
        """処理実行部"""
        while True:
            time.sleep(1)



    