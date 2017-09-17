# -*- utf-8 -*-
import sys
# -*- coding:utf-8 -*-
import socket
import asyncio
from enum import Enum
from concurrent.futures import ThreadPoolExecutor

class ConnectionStatus(Enum):
    DISCONNECTED = 0
    CONNECTED = 1

class TcpClient():
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = '50000'
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #オブジェクトの作成をします
        self._connected = None
        self._discooneted = None
        self.status = ConnectionStatus.DISCONNECTED

    def connect(self, host, port):
        """サーバーへ接続"""
        self.host = host
        self.port = port
        ret = True
        try:
            self._client.connect((self.host, self.port)) #これでサーバーに接続します
            self.status = ConnectionStatus.CONNECTED
            if self._connected is not None:
                self._connected((self.host, self.port))
        except ConnectionRefusedError:
            ret = False
        
        return ret

    def close(self):
        if self.status is ConnectionStatus.CONNECTED:
            self._client.close()

    def sendto(self, data):
        """パケット送信"""
        if self.status is ConnectionStatus.CONNECTED:
            self._client.send(data) 

    def connected_event(self, func):
        """接続ｲﾍﾞﾝﾄ"""
        self._connected = func

    def disconnected_event(self, func):
        """切断ｲﾍﾞﾝﾄ"""
        self._discooneted = func

    def recv(self):
        with ThreadPoolExecutor(max_workers = 128) as tpool:
            try:
                packet = self._client.recv(4096)
            except ConnectionResetError:
                self._client.close()
                self.status = ConnectionStatus.DISCONNECTED
                if self._discooneted is not None:
                    self._discooneted(addr)
            else:
                if not recv_data:
                    self.status = ConnectionStatus.DISCONNECTED
                    if self._discooneted is not None:
                        self._discooneted(addr)
                else:
                    tbool.submit(self.do_proc_packet_worker, recv_data)

    def do_proc_packet_worker(self, recvdata):
        """受信処理用のテンプレート"""
        pass
 
if __name__ == '__main__':
    import time
    import struct
    client = TcpClient()
    if client.connect('127.0.0.1', 50001) is not False:    
        data = struct.pack('16s', 'Hello, World!'.encode('ascii'))
        client.sendto(data)
        client.close()
