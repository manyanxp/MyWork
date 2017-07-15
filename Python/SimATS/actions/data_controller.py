# -*- utf-8 -*-
#-----------------------------------------------------------------------------
import sys, os
print("[*]Append library path: " 
+ os.path.dirname(os.path.abspath(__file__)) + '/../../../Python')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../Python')
#-----------------------------------------------------------------------------
import io
import socket
import time
import threading
import asyncio
from mylibpy.threading.Timer import repeated_timer as rt
from mylibpy.socket import tcp_server as ts
from packet.common_header import IdentificationUnit
from communication import tcp_manager
import resource.defines as defs
#-----------------------------------------------------------------------------

class DataController():
    def __init__(self):
        self.server = tcp_manager.TcpManager.get_instance()
        self.server.recv_packet_event(self._recv_packet_event)
        self.server.bind('0.0.0.0', 10121)
        self.server.listen(5)
        asyncio.ensure_future(self.server.begin_accept_async())

        # ヘルスタイマー登録
        t = rt.RepeatedTimer(3, self._health_send_timer, ["HeathTimer"])
        t.start()

    def _recv_packet_event(*args):
        print("test")

    def _health_send_timer(self, args):
        """ヘルス送信処理"""

        self.server.send_packet("")
        print('ヘルス送信')
