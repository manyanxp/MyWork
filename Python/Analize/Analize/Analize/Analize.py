# -*- utf-8 -*-

import xlrd
import os.path
from datetime import datetime

xlfile = "RecordingItem条件表(A1B3).xls"

class ItemCode():
    def __init__(self, code, name, abbreviated):
        self.code = code
        self.name = name
        self.abbreviated = abbreviated


def convert_to_string(cell):
    if cell.ctype == xlrd.XL_CELL_EMPTY:
        return ''

    if cell.ctype != xlrd.XL_CELL_TEXT:
        return str(cell.value)

    return cell.value

def open_xls(file_pass):
    xls = xlrd.Book()
    if os.path.exists(file_pass):
        xls = xlrd.open_workbook(file_pass)
        return [True, xls]

    return [False, xls]

# アイテムコード取得
def get_item_codes(xls, sheet_name):
    sheet = xls.sheet_by_name(sheet_name)
    nrows = sheet.nrows -1
    ncols = sheet.ncols
    
    codes = []

    for r in range(2, sheet.nrows):

        code = convert_to_string(sheet.cell(r, 0))
        name = convert_to_string(sheet.cell(r, 1))
        abb = convert_to_string(sheet.cell(r,3))

        item = ItemCode(code, name, abb)
        codes.append(item)

    return codes

# Recording Itemのコード値
class RecordingItemCode():
    def __init__(self):
        self.major = ''
        self.sub = ''
        self.detail = ''
        self.locations = []
        self.descs = []

    def to_string(self):
        work = self.major + ',' + self.sub + ',' + self.detail
        for loc in self.locations:
            work += ',' + loc

        for desc in self.descs:
            work += ',' + desc

        return work 
    
class RecordingItem():
    def __init__(self, major, sub, detail, locations, descs):
        self.major = major
        self.sub = sub
        self.detail = detail
        self.locations = self.split_values(locations)
        self.descs = self.split_values(descs)

    def split_values(self, codes):
        values = codes.split(',')
        return values

    def convert_to_recording_item_code(self):
        pass



# アラームアイテムを取得
def get_alarm_items(xls, sheet_name):
    sheet = xls.sheet_by_name(sheet_name)

    major = ''
    sub = ''
    detail = ''
    locations = ''
    desc = ''

    codes = []
    for r in range(2, sheet.nrows):
        work_major = convert_to_string(sheet.cell(r, 1))
        work_sub = convert_to_string(sheet.cell(r, 2))
        work_detail = convert_to_string(sheet.cell(r, 3))
        work_locations = convert_to_string(sheet.cell(r, 4))
        work_desc = convert_to_string(sheet.cell(r, 5))

        if work_major != '':
            major = work_major

        if work_sub != '':
            sub = work_sub

        if work_detail != '':
            detail = work_detail

        if work_locations != '':
            locations = work_locations

        if work_desc != '':
            desc = work_desc

        rec = RecordingItem(major, sub, detail, locations, desc)

        codes.append(rec)

    return codes

class CreateQuerys():
    def __init__(self, codes):
        self.codes = codes

class CreateQuerysForAtsAlarm(CreateQuerys):
    TABLE_NAME = 'KYOSAN_DB.T_ALARM'
    ALARM_FEILDS = 'SEQ_NO,ATS_DEVICE_ID,SEQ_TIME,OCCURRED_TIME,ACKNOW_TIME,RESTORED_TIME,MAJOR_CODE,SUB_CODE,DETAIL_CODE,LOCATION_CODE_1,LOCATION_CODE_2,LOCATION_CODE_3,LOCATION_CODE_4,LOCATION_CODE_5,LOCATION_CODE_6,LOCATION_CODE_7,LOCATION_CODE_8,POS_KIND,TRAIN_NO,DESC_CODE, OPE_ROUTE_CODE'
    def __init__(self, codes):
        return super().__init__(codes)

    def InserAlarmQuesrys(self):
        tdatetime = datetime.today()
        tstr = tdatetime.strftime('%Y/%m/%d %H:%M:%S')
        lists = []
        for code in self.codes:
            sql = 'INSERT INTO '+ self.TABLE_NAME +' (' + self.ALARM_FEILDS + ') VALUES(121,1,TO_DATE(\''+ tstr +'\',\'YYYY-MM-DD HH24:MI:SS\'),TO_DATE(\''+ tstr +'\',\'YYYY-MM-DD HH24:MI:SS\'),TO_DATE(\''+ tstr +'\',\'YYYY-MM-DD HH24:MI:SS\'),TO_DATE(\''+ tstr +'\',\'YYYY-MM-DD HH24:MI:SS\'),\'' + code.major + '\',\'118\',\'118\',\'0000000000000000\',\'0000000000000000\',\'0000000000000000\',\'0000000000000000\',\'0000000000000000\',\'0000000000000000\',\'0000000000000000\',\'0000000000000000\',\'00\',\'8000000000000015\',\'01\',\'02\')'
            lists.append(sql)
        return lists

class AnazlieRecrodingItem():
    def __init__(self, filepath):
        ret, self.xls = open_xls(filepath)
        if ret == False:
            print('File not Found')
            exit

        self.major_codes = get_item_codes(self.xls, 'MAJOR ITEM CODE')
        self.sub_codes = get_item_codes(self.xls, 'SUB ITEM CODE')
        self.detail_codes = get_item_codes(self.xls, 'DETAIL ITEM CODE')
        self.location_codes = get_item_codes(self.xls, 'LOCATION ITEM CODE')
        self.description_codes = get_item_codes(self.xls, 'DESCRIPTION ITEM CODE')

        self.ats_alarms = []
        self.train_alarms = []
        self.others_alarms = []
        
    def SearchMajorItemCode(self, value):
        for code in self.major_codes:
            if code.name == value:
                return code.code.replace('0x','')

        return '00'

    def SearchSubItemCode(self, value):
        for code in self.sub_codes:
            if code.name == value:
                return code.code.replace('0x','')
    
        return '00'

    def SearchDetailItemCode(self, value):
        for code in self.detail_codes:
            if code.name == value:
                temp = code.code.replace('0x','')
                temp = '00' + temp
                return temp

        return '0000'

    def SearchLocationItemCode(self, value):
        for code in self.location_codes:
            if code.name == value:
                return code.code.replace('0x','')

        return '0000000000000000'

    def SearchDescriptionItemCode(self, value):
        for code in self.description_codes:
            if code.name == value:
                return code.code.replace('0x','')

        return '00'

    def extraction_alarm(self):
        recs = get_alarm_items(self.xls, 'ATS Alarm')
        for rec in  recs:
            item = RecordingItemCode()
            item.major = self.SearchMajorItemCode(rec.major)
            item.sub = self.SearchSubItemCode(rec.sub)
            item.detail = self.SearchDetailItemCode(rec.detail)
            
            for value in rec.locations:
                loc = self.SearchLocationItemCode(value)
                item.locations.append(loc)

            for value in rec.descs:
                desc = self.SearchDescriptionItemCode(value)
                item.descs.append(desc)

            print(item.to_string())
            self.ats_alarms.append(item)

        test = CreateQuerysForAtsAlarm(self.ats_alarms)
        q = test.InserAlarmQuesrys()
        print(q[0])


if __name__ == '__main__':
    proc = AnazlieRecrodingItem('test.xls')
    proc.extraction_alarm()
