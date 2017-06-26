#-*- coding: utf-8 -*-

import sys
import io
import socket
import threading
from packet.common_header import IdentificationUnit


class TcpServer:
    def __init__(self, bindip, bindport):
        self.bindip = bindip
        self.bindport = bindport
        self.__server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.__server.bind((self.bindip, self.bindport))

    # Listen
    def listen(self, numbers):
        self.__server.listen(numbers)

        print('[*]Listening on %s:%d' % (self.bindip, self.bindport))

    # Accept
    def accept(self):
            client,addr = self.__server.accept()
            print('[*] Accepted connectoin from: %s:%d' % (addr[0],addr[1]))
            client_handler = threading.Thread(target=handle_client,args=(client,))
            client_handler.daemon = True
            client_handler.start()

    def handle_client(client_socket):

        while True:
            bufsize=1024
            request = client_socket.recv(bufsize)
            do_message_dipatch(request)
    
            #print('[*] Recived: %s' % request)

            #client_socket.send("Hallo Client!!!\n")

        client_socket.close()

    def do_message_dispatch(self, message):
        pass


class MessageWorkder(TcpServer):
    def __init__(self, bindip, bindport):
        super(__class__).__init__(bindip, bindport)

    def do_message_dispatch(self, message):
        buffer = io.BytesIO(request)
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

class App:
    _instance = None
    def __init__(self):
        print('init')

    @classmethod
    def get_instance(cls):
       if cls._instance is None:
            cls._instance = cls()

            return cls._instance

	# 実行部
    def run(self):
        server = TcpServer('0.0.0.0', 10121)
        server.listen(5)
        while True:
            print('start accept')
            server.accept()



