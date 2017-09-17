# -*- conding:utf-8 -*-

import Adafruit_BMP.BMP085 as BMP085

#region Type is AtmosphericInformationModel
class AtmosphericInformationModel:
    '''大気情報モデル'''
    def __init__(self):
        self._sensor = BMP085.BMP085()

        # 気温
        self._temperature = 0.0
        # 気圧
        self._pressure = 0.0
        # 高度
        self._altitude = 0.0
        # 海面気圧
        self._sealevel_pressure = 0.0

    def Temperature(self):
        '''気温'''
        self._temperature = self._sensor.read_temperature()
        return self._temperature

    def Pressure(self):
        '''気圧(未補正)'''
        self._pressure = self._sensor.read_pressure()
        return self._pressure

    def Altitude(self):
        '''高度'''
        self._altitude = self._sensor.read_altitude()
        return self._altitude

    def SealevelPressure(self):
        '''海面気圧'''
        self._sealevel_pressure = self._sensor.read_sealevel_pressure()
        return self._sealevel_pressure

    def ToString(self):
        return "Temperature:%f Pressure: %f Altitude: %f SeaLevel Pressure: %f" % (self.Temperature(), self.Pressure(), self.Altitude(), self.SealevelPressure())

#endregion

if __name__ == '__main__':
    model = AtmosphericInformationModel()
    print(model.Temperature())

    print(model.ToString())

