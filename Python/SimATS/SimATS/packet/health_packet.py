#-*- coding: utf-8 -*-

from common_header import AppHeaderPacket
from common_header import CommonHeaderPacket
from ctypes import LittleEndianStructure
from ctypes import c_byte

# ヘルス情報パケット From ATS
class HealthInfomationPacketFromATS(LittleEndianStructure):
    _pack_ = 4
    _fields_ = [
        ('app_header', AppHeaderPacket),
        ('common_header', CommonHeaderPacket),
        ('data_detail', c_byte * 128)]


