# -*- utf-8 -*-

#-----------------------------------------------------------------------------
import io
import socket
import time
import threading
import asyncio
from threading import Lock
#-----------------------------------------------------------------------------
class TcpServer:
    def __init__(self):
        """通信ソケットの作成"""
        self.clients = []
        self.bindip = "0.0.0.0"
        self.bindport = 500000
        self.lock = Lock()

    def bind(self, bindip, bindport):
        """ソケット作成"""
        self.bindip = bindip
        self.bindport = bindport
        self.__server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.__server.bind((self.bindip, self.bindport))

    # Listen
    def listen(self, numbers):
        """接続待ち"""
        self.__server.listen(numbers)

        print('[*]Listening on %s:%d' % (self.bindip, self.bindport))

    # Accept
    def accept(self):
        """接続要求処理"""
        client,addr = self.__server.accept()
        print('[*]Accepted connectoin from: %s:%d' % (addr[0],addr[1]))

        with self.lock:
            self.clients.append((client, addr))
            client_handler = threading.Thread(target=self.handle_client,args=(client,addr),)
            client_handler.daemon = True
            client_handler.start()

    async def begin_accept_async(self):
        """非同期による接続要求待ち"""
        while True:
            self.accept() 
        return True

    def remove_conection(self, con, addr):
        """クライアントと接続を切る"""
        print('切断{}'.format(addr))
        with self.lock:
            con.close()
            self.clients.remove((con, addr))

    def send_packet(self, messege):
        """クライアントへのパケット送信"""
        with self.lock:
            for c in self.clients:
                c[0].sendto(message, c[1])

    def handle_client(self, con, addr):
        """クライアントハンドル"""

        while True:
            bufsize=1024
            try:
                recv_data = con.recv(bufsize)
            except ConnectionResetError:
                self.remove_conection(con, addr)
                break
            else:
                if not recv_data:
                    self.remove_conection(con, addr)
                    break
                else:
                    asyncio.ensure_future(self.do_proc_packet_async(con, recv_data))

        print('受信処理終了')

    async def do_proc_packet_async(self, client_scoket, message):
        """パケットの非同期処理テンプレート"""
        pass


if __name__ == '__main__':
    server = TcpServer()
    server.bind('0.0.0.0', 50000)
    server.listen(10)
    asyncio.ensure_future(server.begin_accept_async())

