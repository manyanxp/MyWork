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
from packet.health_packet import HealthInfomationPacketToATS
from communication import tcp_manager
import resource.defines as defs

#-----------------------------------------------------------------------------

class DataController():
    def __init__(self):
        self.server = tcp_manager.TcpManager.get_instance()
        self.server.recv_packet_event = self._on_recv_packet
        self.server.bind('0.0.0.0', 10121)
        self.server.listen(5)
        self.server.begin_accept_async()
        
        # ヘルスタイマー登録
        self.healthtimer = rt.RepeatedTimer(3, self._health_send_timer, ["HeathTimer"])
        self.healthtimer.start()
    
    def _on_recv_packet(self, coninfo):
        print("test")
        try:
            a = coninfo.common_header.function_code
        except:
            import traceback
            traceback.print_exc()

        if a == 0:
            print("test2")

        #print("test3")

    def _health_send_timer(self, args):
        """ヘルス送信処理"""

        self.server.send_packet("")
        print('ヘルス送信')
