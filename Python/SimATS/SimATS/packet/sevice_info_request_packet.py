#-*- coding: utf-8 -*-

from common_header import AppHeaderPacket
from common_header import CommonHeaderPacket
from ctypes import LittleEndianStructure
from ctypes import c_byte
from ctypes import c_ushort
from enum import Enum


# Day Chanage Observe Packet
class DayChangeObservePacket(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('app_header', AppHeaderPacket),
        ('common_header', CommonHeaderPacket),
        ('reserve1', c_byte * 4),
        ('now_date', DateTime),
        ('reserve2', c_byte)
        ]


# Log Compress Finishi Packet
class DayChangeObserveAnserPacket(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('app_header', AppHeaderPacket),
        ('common_header', CommonHeaderPacket),
        ('reserve1', c_byte * 4),
      ]


