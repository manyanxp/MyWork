# -*- conding:utf-8 -*-
from pymongo import MongoClient

# Type is DatabaseBase Class
class DatabaseBase:
    _host = "localhost"
    _port = 27017
    _databasename = ""
    _client = None
    _db = None

    def __init__(self, host, port, databasename):
        print (__package__)
        self._host = host
        self._port = port
        self._databasename = databasename

    def Connect(self):
        print("Start connection => %s" % self._host)
        self._client = MongoClient(host = self._host, port = self._port)
        self._db = self._client[self._databasename]

    def IsConnected(slef):
        if self._db != None:
            return True

        return False
