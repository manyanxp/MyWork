#-*- coding: utf-8 -*-

from common_header import AppHeaderPacket
from common_header import CommonHeaderPacket
from ctypes import LittleEndianStructure
from ctypes import c_byte

# Health Infomation Form ATS
class HealthInfomationPacketFromATS(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('app_header', AppHeaderPacket),
        ('common_header', CommonHeaderPacket),
        ('data_detail', c_byte * 128)]


# Health Infomation To ATS
class HealthInfomationPacketToATS(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('app_header', AppHeaderPacket),
        ('common_header', CommonHeaderPacket),
        ('reserve1', c_byte * 4),
        ('starting', c_byte),
        ('my_failure', c_byte),
        ('other_failure1', c_byte),
        ('other_failure2', c_byte),
        ('priority_device', c_byte),
        ('reserve2', c_byte),
        ('reserve3', c_byte),
        ('reserve4', c_byte),
        ('version', c_byte * 8)
        ]




