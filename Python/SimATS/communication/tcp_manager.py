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
from ctypes import sizeof
from mylibpy.socket import tcp_server as ts
from mylibpy.util import convert
from packet import common_header as ch
#-----------------------------------------------------------------------------

class ConnectionInfo():
    def __init__(self, client_socket, recvdata):
        self.client_socket = client_socket
        self.recvdata = recvdata
        self.app_header = ch.AppHeaderPacket.to_struct(recvdata)
        buffer = convert.extract_bytes(recvdata, 0, sizeof(ch.AppHeaderPacket))
        self.common_header = ch.CommonHeaderPacket.to_struct(buffer)
        

class TcpManager(ts.TcpServer):
    _instance = None
    _callback = None
    recv_packet_event = None

    @classmethod
    def get_instance(cls):
       """唯一のインスタンスを返す"""
       if cls._instance is None:
            cls._instance = cls()
            return cls._instance

    def handler(self, *args):
        if self.recv_packet_event is not None:
            self.recv_packet_event(*args)

    def do_proc_packet_worker(self, client_socket, recvdata):
        """パケットの処理
           スレッドプールに登録されて起動する。
        """   
        coninfo = ConnectionInfo(client_socket, recvdata)
        self.handler(coninfo)

