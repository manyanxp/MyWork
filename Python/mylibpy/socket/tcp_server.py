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
        self.bindport = 50000
        self._lock = Lock()

        self._connected = None
        self._discooneted = None

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

        with self._lock:
            self.clients.append((client, addr))
            client_handler = threading.Thread(target=self.handle_client,args=(client,addr),)
            client_handler.daemon = True
            client_handler.start()
            if self._connected is not None:
                self._connected((client,addr))
    
    async def _begin_accept_async(self, loop):
        """非同期による接続要求待ち（本体）"""
        while True:
            self.accept() 

    def begin_accept_async(self):
        """非同期による接続要求待ち"""
        loop = asyncio.get_event_loop()
        asyncio.ensure_future(self._begin_accept_async(loop))
        loop.run_forever()

    def remove_conection(self, con, addr):
        """クライアントと接続を切る"""
        print('切断{}'.format(addr))
        with self._lock:
            con.close()
            self.clients.remove((con, addr))

    def send_packet(self, messege):
        """クライアントへのパケット送信"""
        with self._lock:
            for c in self.clients:
                c[0].sendto(message, c[1])

    def connected_event(self, func):
        """接続ｲﾍﾞﾝﾄ"""
        self._connected = func

    def disconnected_event(self, func):
        """切断ｲﾍﾞﾝﾄ"""
        self._discooneted = func

    def handle_client(self, con, addr):
        """クライアントハンドル"""

        while True:
            bufsize=1024
            try:
                recv_data = con.recv(bufsize)
            except ConnectionResetError:
                self.remove_conection(con, addr)
                if self._discooneted is not None:
                    self._discooneted(addr)
                break
            else:
                if not recv_data:
                    self.remove_conection(con, addr)
                    if self._discooneted is not None:
                        self._discooneted(addr)
                    break
                else:
                    loop = asyncio.get_event_loop()
                    asyncio.ensure_future(self.do_proc_packet_async(con, recv_data))
                    loop.run_forever()

        print('[*] 受信処理終了')

    async def do_proc_packet_async(self, client_scoket, message):
        """パケットの非同期処理テンプレート"""
        pass

def disconnected(*arg):
    print(arg[0])

if __name__ == '__main__':
    server = TcpServer()
    server.bind('0.0.0.0', 50001)
    server.listen(10)
    #server.accept()
    server.disconnected_event(disconnected)
    server.begin_accept_async()


    while True:
        time.sleep(3)


