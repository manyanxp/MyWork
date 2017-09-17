# -*- config: utf-8 -*-
from Weather.WeatherStationIF.interface_atom import IAtomsphericInfomationModel

class TestAtmosphericInformationModel(IAtomsphericInfomationModel):
    """テストモデル"""
    def __init__(self):
        self.temperature = 0.0
        self.pressure = 0.0
        self.altitude = 0.0
        self.sealevel_pressure = 0.0

        # 気温
    def Temperature(self):
        return self.temperature

        # 気圧
    def Pressure(self):
        return self.pressure

    def Altitude(self):
        return self.altitude

    def SealevelPressure(self):
        return self.sealevel_pressure

if __name__ == '__main__':
    test = TestAtmosphericInformationModel()


