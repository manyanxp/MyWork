#-*- coding: utf-8 -*-

from common_header import AppHeaderPacket
from common_header import CommonHeaderPacket
from ctypes import LittleEndianStructure
from ctypes import c_byte
from ctypes import c_ushort
from enum import Enum

# ReportOutoutRequeset Packet
class ReportOutoutRequesetPacket(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('app_header', AppHeaderPacket),
        ('common_header', CommonHeaderPacket),
        ('reserve1', c_byte * 4),
        ('vehicle_id1', c_byte),
        ('vehicle_id2', c_byte),
        ('vehicle_id3', c_byte),
        ('reserve1', c_byte * 9)
        ]


# ReportOutoutRequesetAnser Packet
class ReportOutoutRequesetAnserPacket(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('app_header', AppHeaderPacket),
        ('common_header', CommonHeaderPacket),
        ('reserve1', c_byte * 4),
        ]


