# -*- conding:utf-8 -*-

#region Type is AtmosphericInformation
class AtmosphericInformation:
    def __init__(self):
        # 気温
        self.Temperature = 0.0
        # 気圧
        self.Pressure = 0.0
        # 高度
        self.Altitude = 0.0

    def ToString(self):
        return "Temperature:%f Pressure: %f Altitude: %f " % (self.Temperature, self.Pressure, self.Altitude)

#endregion
