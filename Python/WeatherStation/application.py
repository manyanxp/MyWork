# -*- config: utf-8 -*-
#------------------------------------------------------------
from Weather.WeatherStation import Weatherstation, WeatherInfomation, WeatherInfomationKind
from Weather.DataModel.DataModel import AtmosphericInformationModel
from Weather.TestModel.test_atom_info import TestAtmosphericInformationModel
from datetime import date

# アプリケーションメイン
class App:
    _instance = None
    def __init__(self):
        """アプリケーションの初期化処理"""

        print('[*]Begin... Initalize application')
        self._initalize_resource()

    @classmethod
    def get_instance(cls):
       """唯一のインスタンスを返す"""
       if cls._instance is None:
            cls._instance = cls()
            return cls._instance


    def _initalize_resource(self):
        """何かｱﾌﾟﾘの初期化処理があれば記述"""
        pass

	# 実行部
    def run(self):
        """処理実行部"""
        station = Weatherstation('192.168.1.201', 27017, 'weatherstation', 'AtmosphericInformation')
        #station.Test()
        model = AtmosphericInformationModel()
        info = WeatherInfomation(date.today(), WeatherInfomationKind.Normal.value, model)
        station.Insert(info)
        station.Select(date.today(), date.today())

        test = TestAtmosphericInformationModel()
        test.temperature = 1.0
        print(test.Temperature())
 