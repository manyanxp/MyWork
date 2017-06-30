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


# AlarmData Structure
class AlarmData(LittleEndianStructure):
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
        ('operater_name_and_level', c_byte * 22),
        ('computer_work_area', c_byte * 12),
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
class AlarmListInfomationPacket(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('app_header', AppHeaderPacket),
        ('common_header', CommonHeaderPacket),
        ('reserve1', c_byte * 4),
        ('numberof_alarm_regists', c_ushort),
        ('end_flg', c_byte),
        ('reserve2', c_byte),
        ('static_data',  AlarmData)
        ]


# Alarm List Infomation Anser & Anser Code
class AlarmListInfomationAnserCode(Enum):
    OK = 0


class AlarmListInfomationAnserPacket(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('app_header', AppHeaderPacket),
        ('common_header', CommonHeaderPacket),
        ('reserve1', c_byte * 4)
        ]


