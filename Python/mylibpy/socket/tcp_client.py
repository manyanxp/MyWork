# -*- utf-8 -*-
import sys
# -*- coding:utf-8 -*-
import socket
import asyncio

class TcpClient():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #オブジェクトの作成をします
        self._connected = None
        self._discooneted = None

    def connect(self):
        """サーバーへ接続"""
        ret = True
        try:
            self.__client.connect((self.host, self.port)) #これでサーバーに接続します
            if self._connected is not None:
                self._connected((self.host, self.port))
        except ConnectionRefusedError:
            ret = False
        
        return ret

    def close(self):
        self.close()

    def sendto(self, data):
        """パケット送信"""
        self.__client.send(data) 

    def connected_event(self, func):
        """接続ｲﾍﾞﾝﾄ"""
        self._connected = func

    def disconnected_event(self, func):
        """切断ｲﾍﾞﾝﾄ"""
        self._discooneted = func

    def recv(self):
        try:
            packet = self.__client.recv(4096)
        except ConnectionResetError:
            self.__client.close()
        else:
            if not recv_data:
                self.remove_conection(con, addr)
                if self._discooneted is not None:
                    self._discooneted(addr)
            else:
                loop = asyncio.get_event_loop()
                asyncio.ensure_future(self.recv_async(packet, loop))
                loop.run_forever()

    async def recv_async(self, recvdata):
        pass
 
if __name__ == '__main__':
    import time

    client = TcpClient('127.0.0.1', 50001)
    if client.connect() is not False:    
        client.sendto("tetestset")
        client.close()
