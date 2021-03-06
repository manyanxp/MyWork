#-*- coding: utf-8 -*-

from common_header import AppHeaderPacket
from common_header import CommonHeaderPacket
from common_header import DateTime
from ctypes import LittleEndianStructure
from ctypes import c_byte
from ctypes import c_ushort
from enum import Enum


# DRR Wakeup Packet
class DrrWakeupPacket(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('app_header', AppHeaderPacket),
        ('common_header', CommonHeaderPacket),
        ('reserve1', c_byte * 4),        
        ]

# DRR Wakeup Anser Packet
class DrrWakeupAnserPacket(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('app_header', AppHeaderPacket),
        ('common_header', CommonHeaderPacket),
        ('reserve1', c_byte * 4),
        ('now_date', DateTime),
        ('reserve1', c_byte)
        ]


