#-*- coding: utf-8 -*-

from ctypes import LittleEndianStructure
from ctypes import c_uint32
from ctypes import c_byte

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

