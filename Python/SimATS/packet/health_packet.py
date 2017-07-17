#-*- coding: utf-8 -*-

import io
from .common_header import IdentificationUnit
from .common_header import AppHeaderPacket
from .common_header import CommonHeaderPacket
from ctypes import LittleEndianStructure
from ctypes import c_byte
from ctypes import sizeof

# Health Infomation Form ATS
class HealthInfomationPacketFromATS(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('app_header', AppHeaderPacket),
        ('common_header', CommonHeaderPacket),
        ('data_detail', c_byte * 128)]

    def to_struct(self, binary):
        buffer = io.BytesIO(message)
        packet = HealthInfomationPacketFromATS()
        buffer.readinto(packet)
        return packet

    def to_binary(self, structure):
        buffer = io.BytesIO()
        buffer.write(structure)
        return buffer.getvalue()


# Health Infomation To ATS
class HealthInfomationPacketToATS(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('app_header', AppHeaderPacket),
        ('common_header', CommonHeaderPacket),
        ('reserve1', c_byte * 4),
        ('starting', c_byte),
        ('my_failure', c_byte),
        ('other_failure1', c_byte),
        ('other_failure2', c_byte),
        ('priority_device', c_byte),
        ('reserve2', c_byte),
        ('reserve3', c_byte),
        ('reserve4', c_byte),
        ('version', c_byte * 8)
        ]

    def to_struct(self, binary):
        buffer = io.BytesIO(binary)
        packet = HealthInfomationPacketToATS()
        buffer.readinto(packet)
        return packet

    def to_binary(self):
        buffer = io.BytesIO()
        self.app_header.identification_unit.data_size = sizeof(HealthInfomationPacketToATS) - sizeof(IdentificationUnit)
        self.app_header.identification_unit.data_id  = ~self.app_header.identification_unit.data_size
        buffer.write(self)
        return buffer.getvalue()
