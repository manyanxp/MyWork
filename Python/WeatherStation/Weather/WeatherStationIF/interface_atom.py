#-*- config: utf-8 -*-

class IAtomsphericInfomationModel(object):
    """大気モデル インターフェース"""
    
    # 気温
    def Temperature(self):
        pass

        # 気圧
    def Pressure(self):
        pass

    def Altitude(self):
        pass

    def SealevelPressure(self):
        pass