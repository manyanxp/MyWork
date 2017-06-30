#-*- coding: utf-8 -*-

from common_header import AppHeaderPacket
from common_header import CommonHeaderPacket
from common_header import DateTime
from ctypes import LittleEndianStructure
from ctypes import c_byte
from ctypes import c_ushort
from enum import Enum


# Alarm Status Request Packet
class AlarmStatusRequestPacket(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('app_header', AppHeaderPacket),
        ('common_header', CommonHeaderPacket),
        ('reserve1', c_byte * 4),        
        ]

# Alarm Status Request Anser Packet
class AlarmStatusRequestAnserPacket(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('app_header', AppHeaderPacket),
        ('common_header', CommonHeaderPacket),
        ('reserve1', c_byte * 4),
        ]


