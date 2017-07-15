#-*- coding: utf-8 -*-

from common_header import AppHeaderPacket
from common_header import CommonHeaderPacket
from common_header import DateTime
from ctypes import LittleEndianStructure
from ctypes import c_byte
from ctypes import c_ushort
from enum import Enum



# Location Structure
class Location(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('field1', c_byte),
        ('field2', c_byte),
        ('field3', c_byte),
        ('field4', c_byte),
        ('field5', c_byte),
        ('field6', c_byte),
        ('field7', c_byte),
        ('field8', c_byte)
        ]


# StaticesDataDetail Structure
class StaticsDataDetail(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('date_time', DateTime),
        ('data_kind', c_byte),
        ('cyclic_counter', c_ushort),
        ('operation_device_id', c_byte),
        ('route_code', c_byte),
        ('major_itme', c_byte),
        ('sub_item', c_byte),
        ('detail_itme', c_ushort),
        ('description', c_byte),
        ('priority', c_byte),
        ('buzer_kind', c_byte),
        ('ack_flg', c_byte),
        ('locations', Location * 8),
        ('operater_name', c_byte * 22),
        ('password', c_byte * 8),
        ('access_level', c_byte),
        ('reserve1', c_byte),
        ('occured_date_time', DateTime),
        ('reserve2', c_byte),
        ('occured_cyclic_counter', c_ushort),
        ('reserve3', c_byte),
        ('reserve4', c_byte)
        ]


# Weather Location
class WeatherLocation(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('alarm_info', c_ushort),
        ('wind_forth', c_ushort),
        ('wind_direction', c_ushort),
        ('precipitantion', c_ushort),
        ('temperature', c_ushort),
        ('humidity', c_ushort),
        ('route_code', c_byte),
        ('reserve1', c_byte),
        ('reserve2', c_byte),
        ('reserve3', c_byte),
        ]

# Weather Log
class WeatherLog(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('alarm_info', c_ushort),
        ('locations', WeatherLocation * 2),
        ('reserve1', c_byte * 16),
        ('computer_work_area', c_byte * 12)
        ]

# StaticsData
class StaticsDataPacket(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('app_header', AppHeaderPacket),
        ('common_header', CommonHeaderPacket),
        ('counts', c_ushort),
        ('reserve1', c_byte),
        ('reserve2', c_byte),
        ('static_data',  StaticsDataDetail)]


# StaticsDataAnser
class StaticsDataAnserCode(Enum):
    OK = 0
    DatabaseRegistErr = 1
    DatabaseUpdateErr = 2
    ReceivedSameData = 3
    NotReceivedOccur = 4
    KindOrItemValueErr = 5

class StaticsDataAnserPacket(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('app_header', AppHeaderPacket),
        ('common_header', CommonHeaderPacket),
        ('reserve1', c_byte * 4)
        ]


