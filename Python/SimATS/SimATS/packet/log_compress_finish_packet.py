#-*- coding: utf-8 -*-

from common_header import AppHeaderPacket
from common_header import CommonHeaderPacket
from ctypes import LittleEndianStructure
from ctypes import c_byte
from ctypes import c_ushort
from enum import Enum


# Log Compress Finishi Packet
class LogCompressFinishPacket(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('app_header', AppHeaderPacket),
        ('common_header', CommonHeaderPacket),
        ('reserve1', c_byte * 4),
        ('ats_device_number', DateTime),
        ('situation_kind', c_byte),
        ('reserve3', c_byte),
        ('reserve4', c_byte),
        ('file_path', c_byte * 256),
        ]


# Log Compress Finishi Packet
class LogCompressFinishAnserPacket(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('app_header', AppHeaderPacket),
        ('common_header', CommonHeaderPacket),
        ('reserve1', c_byte * 4),
        ('situation_kind', c_byte),
        ('reserve2', c_byte),
        ('reserve3', c_byte),
        ('reserve4', c_byte),
        ]


