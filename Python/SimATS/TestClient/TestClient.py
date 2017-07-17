# -*- utf-8 -*-
#-----------------------------------------------------------------------------
import sys, os
print("[*]Append library path: " 
+ os.path.dirname(os.path.abspath(__file__)) + '/../../../Python')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../Python')
#-----------------------------------------------------------------------------

import io
import datetime
from mylibpy.socket import tcp_client as tc
from mylibpy.util import convert
from SimATS.packet.health_packet import HealthInfomationPacketToATS

class TestClient(tc.TcpClient):
    _instance = None
    def __init__(self):
        return super().__init__()

    def get_instance(cls):
        if cls._instance is None:
            cls._instance = TestClient()
            return cls._instance
        
    def send_packet(self, senddata):
        today = datetime.datetime.now()
        senddata.app_header.year = 0x000000FF & convert.to_bcd(today.year)
        senddata.app_header.month = today.month
        senddata.app_header.day = today.day
        senddata.app_header.hour = today.hour
        senddata.app_header.minute = today.minute
        senddata.app_header.second = today.second
        self.sendto(senddata.to_binary())

    def recv_packet_event(self, func):
        """受信時のイベント"""
        self._callback = func
    
    def do_proc_packet_worker(self, recvdata):
        pass


def recv_packet(*argv):
    print('test')

if __name__ == '__main__':
    client = TestClient()
    client.recv_packet_event(recv_packet)
    
    health = HealthInfomationPacketToATS()
    health.starting = 1
    health.my_failure = 0x03
    health.version[0] = 0x10
    
    client.connect('127.0.0.1', 10121)
    packet = health.to_binary()
    client.send_packet(health)
    client.close()

    