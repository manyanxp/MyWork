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
from mylibpy.socket import tcp_server as ts
from packet.common_header import IdentificationUnit
#-----------------------------------------------------------------------------

class TcpManager(ts.TcpServer):
    _instance = None
    _callback = None

    @classmethod
    def get_instance(cls):
       """唯一のインスタンスを返す"""
       if cls._instance is None:
            cls._instance = cls()
            return cls._instance

    def recv_packet_event(self, func):
        self._callback = func

    async def do_proc_packet_async(self, client_socket, message):
        """パケットの非同期処理"""

        buffer = io.BytesIO(message)
        t = IdentificationUnit()
        buffer.readinto(t)

        print(t.data_id)
        print(t.data_size)

        if self._callback is not None:
            self._callback(t)

        #print(t.app_header.identification_unit.data_id)
        #print(t.app_header.identification_unit.data_size)
        #print(t.common_header.device_id)
        #print(t.common_header.function_code)
        #print(t.common_header.item_code)
        #print(t.data_detail)
