# -*- conding:utf-8 -*-

import Adafruit_BMP.BMP085 as BMP085

#region Type is AtmosphericInformationModel
class AtmosphericInformationModel(IAtomsphericInfomationModel):
    '''大気情報モデル'''
    def __init__(self):
        self.__sensor = BMP085.BMP085()

        # 気温
        self.__temperature = 0.0
        # 気圧
        self.__pressure = 0.0
        # 高度
        self.__altitude = 0.0
        # 海面気圧
        self.__sealevel_pressure = 0.0

    def Temperature(self):
        """気温"""
        self.__temperature = self.__sensor.read_temperature()
        return self.__temperature

    def Pressure(self):
        """気圧(未補正)"""
        self.__pressure = self.__sensor.read_pressure()
        return self.__pressure

    def Altitude(self):
        """高度"""
        self.__altitude = self.__sensor.read_altitude()
        return self.__altitude

    def SealevelPressure(self):
        """海面気圧"""
        self.__sealevel_pressure = self.__sensor.read_sealevel_pressure()
        return self.__sealevel_pressure

    def ToString(self):
        return "Temperature:%f Pressure: %f Altitude: %f SeaLevel Pressure: %f" % (self.Temperature(), self.Pressure(), self.Altitude(), self.SealevelPressure())

#endregion

if __name__ == '__main__':
    model = AtmosphericInformationModel()
    print(model.Temperature())

    print(model.ToString())

