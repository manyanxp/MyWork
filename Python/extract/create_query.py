# -*- utf-8 -*-
from datetime import datetime
from datetime import timedelta

# クエリー作成
class CreateQuerys():
    DATETIME_FORMAT = 'YYYY-MM-DD HH24:MI:SS'
    def __init__(self, codes):
        self.codes = codes


# クエリー作成（ATS Alarm）
class CreateQuerysForAtsAlarm(CreateQuerys):
    TABLE_NAME = 'KYOSAN_DB.T_ALARM'
    ALARM_FEILDS = 'SEQ_NO,ATS_DEVICE_ID,SEQ_TIME,OCCURRED_TIME,ACKNOW_TIME,RESTORED_TIME,MAJOR_CODE,SUB_CODE,DETAIL_CODE,LOCATION_CODE_1,LOCATION_CODE_2,LOCATION_CODE_3,LOCATION_CODE_4,LOCATION_CODE_5,LOCATION_CODE_6,LOCATION_CODE_7,LOCATION_CODE_8,POS_KIND,TRAIN_NO,DESC_CODE, OPE_ROUTE_CODE'
    def __init__(self, codes):
        return super().__init__(codes)

    # ATS AlarmのInsert文
    def insert_alarm_query(self):
        tdatetime = datetime.today()

        lists = []
        seq = 1
        for code in self.codes:
            tdatetime = tdatetime + timedelta   (seconds=seq)
            tstr = tdatetime.strftime('%Y/%m/%d %H:%M:%S')
             
            sql = 'INSERT INTO '+ self.TABLE_NAME +' (' + self.ALARM_FEILDS + ')' 
            sql +='VALUES('+ str(seq) +',1,TO_DATE(\''+ tstr +'\',\''+ CreateQuerys.DATETIME_FORMAT  +'\'),TO_DATE(\''+ tstr +'\',\''+ CreateQuerys.DATETIME_FORMAT +'\'),TO_DATE(\''+ tstr +'\',\'' + CreateQuerys.DATETIME_FORMAT + '\'),TO_DATE(\''+ tstr +'\',\'' + CreateQuerys.DATETIME_FORMAT + '\'),\''
            sql += code.major + '\',\''+ code.sub + '\',\'' + code.detail + '\',\''
            sql += code.locations[0] +'\',\''+ code.locations[1] +'\',\''+ code.locations[2] +'\',\''+ code.locations[3] +'\',\''
            sql += code.locations[4] +'\',\''+ code.locations[5] +'\',\''+ code.locations[6] +'\',\''+ code.locations[7] +'\',\'00\',\'8000000000000015\',\''+ code.descs[0] +'\',\'02\')'
            lists.append(sql)
            seq +=1

        return lists
