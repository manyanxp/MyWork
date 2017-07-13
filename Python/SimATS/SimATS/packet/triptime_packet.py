#-*- coding: utf-8 -*-

from common_header import AppHeaderPacket
from common_header import CommonHeaderPacket
from common_header import DateTime
from common_header import TrainId
from ctypes import LittleEndianStructure
from ctypes import c_byte
from ctypes import c_ushort
from enum import Enum

# Between Station Data
class BetweenStationData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('dept_station', c_byte),
        ('arrive_station', c_byte),
        ('dwell_time', c_byte),
        ('reserve1', c_byte),
        ('trip_time', c_ushort),
        ('reserve2', c_byte),
        ('reserve3', c_byte)
        ]


# TripTime Packet
class TripTimePacket(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('app_header', AppHeaderPacket),
        ('common_header', CommonHeaderPacket),
        ('reserve1', c_byte * 4),
        ('occured_datetime', DateTime),
        ('reserve2', c_byte),
        ('route_code',  c_byte),
        ('service_mode', c_byte),
        ('reserve3', c_byte),
        ('reserve4', c_byte),
        ('train_id', TrainId),
        ('rtt', c_ushort),
        ('reserve5', c_byte),
        ('reserve6', c_byte),
        ]


