# -*- conding:utf-8 -*-
from datetime import date
from Database.DatabaseBase import DatabaseBase
from . import DataModel
from enum import Enum

#region Type is weatherinfomation kind
class WeatherInfomationKind(Enum):
    # 通常
    Normal = 1
    # 変化
    Change = 2
#endregion

#region Type if WeatherInfomation
class WeatherInfomation:
    date = None
    kind = 0
    atom = None
    def __init__(self, date, kind, atom):
        self.date = date
        self.kind = kind
        self.atom = atom
#endregion

#region Type is WeatherStatoin Class
class Weatherstation(DatabaseBase):
    # コレクション名
    _collectionname = ""
    # コレクション
    _collection = None
    def __init__(self, host, port, databasename, collectionname):
        super(Weatherstation, self).__init__(host, port, databasename)

        print ("host:%s port:%d" % (host, port))

        # mongodbに接続
        self.Connect()
        # コレクション取得
        self._collectionname = collectionname
        self._collection = self._db[self._collectionname]

    # Insert wather infomation
    def Insert(self, info):
        if self.IsConnected == False:
            print("Not Connected.")
            return

        col = self._collection
        col.insert_one({'Kind':info.kind, 'Temperature':info.atom.Temperature})
        print("Insert => %s" % info.atom.ToString())

    # Select weather infomation by startdate and enddate
    def Select(self, startdate, enddate):
        if self.IsConnected == False:
            print("Not Connected.")
            return

        col = self._collection
        for data in col.find({u'Temperature':1.0}):
            print (data)

    def Test(self):
        col = self._collection
        col.insert_one({'x':1})

        print ("=====find_one=====")
        print (col.find_one())

        print ("=====find=====")
        for data in col.find():
            print (data)

        print ("=====find_query=====")
        for data in col.find({u'a':10}):
            print (data)
#endregion
