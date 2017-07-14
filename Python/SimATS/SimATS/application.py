#-*- coding: utf-8 -*-

import sys
import io
import socket
import time
import threading
import signal
from packet.common_header import IdentificationUnit


class TcpServer:
    def __init__(self, bindip, bindport):
        """通信ソケットの作成"""
        self.clients = []
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
        self.clients.append((client, addr))
        client_handler = threading.Thread(target=self.handle_client,args=(client,addr),)
        client_handler.daemon = True
        client_handler.start()

    def remove_conection(self, con, addr):
        """クライアントと接続を切る"""
        print('切断{}'.format(addr))
        con.close()
        self.clients.remove((con, addr))

    def send_packet(self, messege):
        """クライアントへのパケット送信"""
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
                    self.do_message_dispatch(con, recv_data)

        print('受信処理終了')

    def do_message_dispatch(self, client_scoket, message):
        pass


class MessageWorkder(TcpServer):
    def __init__(self, bindip, bindport):
        return super().__init__(bindip, bindport)

    def do_message_dispatch(self, client_socket, message):
        buffer = io.BytesIO(message)
        t = IdentificationUnit()
        buffer.readinto(t)

        print(t.data_id)
        print(t.data_size)

        #print(t.app_header.identification_unit.data_id)
        #print(t.app_header.identification_unit.data_size)
        #print(t.common_header.device_id)
        #print(t.common_header.function_code)
        #print(t.common_header.item_code)
        #print(t.data_detail)
        pass

# アプリケーションメイン
class App:
    _instance = None
    def __init__(self):
        """アプリケーションの初期化処理"""

        print('Begin... Initalize application')
        self._initalize_resource()

        self.server = MessageWorkder('0.0.0.0', 10121)

        # ヘルスタイマー登録
        signal.signal(signal.SIGALRM, self._health_send_timer)
        signal.setitimer(signal.ITIMER_REAL, 10, 10)

    @classmethod
    def get_instance(cls):
       if cls._instance is None:
            cls._instance = cls()

            return cls._instance

    def _initalize_resource(self):
        """何かｱﾌﾟﾘの初期化処理があれば記述"""
        pass

	# 実行部
    def run(self):
        """
            処理実行部
        """
        self.server.listen(5)
        while True:
            self.server.accept()

    def _health_send_timer(self):
        print('ヘルス送信')


    