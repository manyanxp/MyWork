#-*- coding: utf-8 -*-

from ctypes import LittleEndianStructure
from ctypes import c_uint32
from ctypes import c_ushort
from ctypes import c_byte

# DateTime Structure
class DateTime(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('year_hi', c_byte),
        ('year_low', c_byte),
        ('month', c_byte),
        ('day', c_byte),
        ('hour', c_byte),
        ('minitues', c_byte),
        ('secondes', c_byte)
        ]

# Train ID
class TrainId(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('date', c_ushort),
        ('vehicle_id1', c_byte),
        ('vehicle_id2', c_byte),
        ('vehicle_id3', c_byte),
        ('vehicle_id4', c_byte),
        ('vehicle_id5', c_byte),
        ('vehicle_id6', c_byte),
        ('seq_no', c_byte),
        ('direction', c_byte),
        ('reserve1', c_byte),
        ('reserve2', c_byte)
        ]


# 識別部ヘッダー
class IdentificationUnit(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('data_id', c_uint32),
        ('data_size', c_uint32)]


# アプリケーションヘッダー
class AppHeaderPacket(LittleEndianStructure):
    _pack_ = 1
    _fields_  = [
        ('identification_unit', IdentificationUnit),
        ('message_seqno_ver', c_uint32),
        ('message_send_seqno', c_uint32),
        ('data_type', c_byte),
        ('block_seqno', c_byte),
        ('reserve1', c_byte),
        ('reserve2', c_byte),
        ('text_data_len', c_uint32),
        ('year', c_byte),
        ('month', c_byte),
        ('day', c_byte),
        ('hour', c_byte),
        ('minute', c_byte),
        ('seconde', c_byte),
        ('reserve3', c_byte),
        ('reserve4', c_byte)]


# 共通ヘッダー
class CommonHeaderPacket(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('device_id', c_byte),
        ('function_code', c_byte),
        ('item_code', c_byte),
        ('anser_code', c_byte)]

