# -*- utf-8 -*-
#-----------------------------------------------------------------------------
# 自作ライブラリパス追加
import sys,os
print(os.path.dirname(os.path.abspath(__file__)) + '/../mylibpy')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../mylibpy')
#-----------------------------------------------------------------------------

import xlrd
import os.path
import xls_io
from diagnostics import stopwatch

#-----------------------------------------------------------------------------

# アイテムコード
class ItemCode():
    def __init__(self, code, name, abbreviated):
        self.code = code
        self.name = name
        self.abbreviated = abbreviated


# 文字列への変換
def convert_to_string(cell):
    if cell.ctype == xlrd.XL_CELL_EMPTY:
        return ''

    if cell.ctype != xlrd.XL_CELL_TEXT:
        return str(cell.value)

    return cell.value


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


# アラームアイテムを取得
def get_recording_items(xls, sheet_name):
    sheet = xls.sheet_by_name(sheet_name)

    major = ''
    sub = ''
    detail = ''
    locations = ''
    desc = ''

    codes = []
    for row in range(2, sheet.nrows):
        work_major = convert_to_string(sheet.cell(row, 1))
        work_sub = convert_to_string(sheet.cell(row, 2))
        work_detail = convert_to_string(sheet.cell(row, 3))
        work_locations = convert_to_string(sheet.cell(row, 4))
        work_desc = convert_to_string(sheet.cell(row, 5))

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


# Recording Itemのコード値
class RecordingItemCode():
    def __init__(self):
        self.major = '00'
        self.sub = '00'
        self.detail = '00'
        self.locations = ['0000000000000000' for i in range(8)]
        self.descs = ['00' for i in range(8)]

    def to_string(self):
        work = self.major + ',' + self.sub + ',' + self.detail
        for loc in self.locations:
            work += ',' + loc

        for desc in self.descs:
            work += ',' + desc

        return work 


 # Recrding Item
class RecordingItem():
    def __init__(self, major, sub, detail, locations, descs):
        self.major = major
        self.sub = sub
        self.detail = detail
        self.locations = self.split_values(locations)
        self.descs = self.split_values(descs)

    # ﾃﾞｰﾀ分割
    def split_values(self, codes):
        values = codes.split(',')
        return values

    def to_string(self):
        work = self.major + ',' + self.sub + ',' + self.detail
        for loc in self.locations:
            work += ',' + loc

        for desc in self.descs:
            work += ',' + desc

        return work 


# Recording Itemの抽出
class ExtractRecrodingItem():
    def __init__(self, filepath):
        sw = stopwatch.Stopwatch()
        sw.start()
        ret, self.xls = xls_io.open_xls(filepath)
        if ret == False:
            print('File not Found')
            sw.end()
            print('処理時間:{0:d}'.format(sw.elapsed_time))
            exit
        
        sw.end()
        print('エクセルを開く時間:{0:f}'.format(sw.elapsed_time))

        # Item Codes
        self.major_codes = get_item_codes(self.xls, 'MAJOR ITEM CODE')
        self.sub_codes = get_item_codes(self.xls, 'SUB ITEM CODE')
        self.detail_codes = get_item_codes(self.xls, 'DETAIL ITEM CODE')
        self.location_codes = get_item_codes(self.xls, 'LOCATION ITEM CODE')
        self.description_codes = get_item_codes(self.xls, 'DESCRIPTION ITEM CODE')

        # Converted Recording Item 
        self.ats_alarms = []
        self.train_alarms = []
        self.others_alarms = []
        self.operations = []
        self.operation_historys = []

    # corvert to binary code
    def convert_majoritem_code(self, value):
        for code in self.major_codes:
            if code.name == value:
                return code.code.replace('0x','')

        return '00'

    def convert_subitem_code(self, value):
        for code in self.sub_codes:
            if code.name == value:
                return code.code.replace('0x','')
    
        return '00'

    def convert_detailitem_code(self, value):
        for code in self.detail_codes:
            if code.name == value:
                temp = code.code.replace('0x','')
                temp = '00' + temp
                return temp

        return '0000'

    def convert_locationitem_code(self, value):
        for code in self.location_codes:
            if code.name == value:
                return code.code.replace('0x','')

        return '0000000000000000'

    def convert_descriptionitem_code(self, value):
        for code in self.description_codes:
            if code.name == value:
                return code.code.replace('0x','')

        return '00'

    # Extract Recording Item for ATS Alarm
    def extract_ats_alarm(self):
        recs = get_recording_items(self.xls, 'ATS Alarm')
        for rec in  recs:
            item = RecordingItemCode()
            item.major = self.convert_majoritem_code(rec.major)
            item.sub = self.convert_subitem_code(rec.sub)
            item.detail = self.convert_detailitem_code(rec.detail)
            
            for idx in range(len(rec.locations)):
                loc = self.convert_locationitem_code(rec.locations[idx])
                item.locations[idx] = loc

            for idx in range(len(rec.descs)):
                desc = self.convert_descriptionitem_code(rec.descs[idx])
                item.descs[idx] = desc

            print(item.to_string())
            self.ats_alarms.append(item)

    # Extract Recording Item for Train Alarm
    def extract_train_alarm(self):
        recs = get_recording_items(self.xls, 'Train Alarm')
        for rec in  recs:
            item = RecordingItemCode()
            item.major = self.convert_majoritem_code(rec.major)
            item.sub = self.convert_subitem_code(rec.sub)
            item.detail = self.convert_detailitem_code(rec.detail)
            
            for idx in range(len(rec.locations)):
                loc = self.convert_locationitem_code(rec.locations[idx])
                item.locations[idx] = loc

            for idx in range(len(rec.descs)):
                desc = self.convert_descriptionitem_code(rec.descs[idx])
                item.descs[idx] = desc

            print(item.to_string())
            self.train_alarms.append(item)

    # Extract Recording Item for Others Alarm
    def extract_others_alarm(self):
        recs = get_recording_items(self.xls, 'Others Alarm')
        for rec in  recs:
            item = RecordingItemCode()
            item.major = self.convert_majoritem_code(rec.major)
            item.sub = self.convert_subitem_code(rec.sub)
            item.detail = self.convert_detailitem_code(rec.detail)
            
            for idx in range(len(rec.locations)):
                loc = self.convert_locationitem_code(rec.locations[idx])
                item.locations[idx] = loc

            for idx in range(len(rec.descs)):
                desc = self.convert_descriptionitem_code(rec.descs[idx])
                item.descs[idx] = desc

            print(item.to_string())
            self.others_alarms.append(item)

    # Extract Recording Item for Operation
    def extract_operation(self):
        recs = get_recording_items(self.xls, 'Operation')
        for rec in  recs:
            item = RecordingItemCode()
            item.major = self.convert_majoritem_code(rec.major)
            item.sub = self.convert_subitem_code(rec.sub)
            item.detail = self.convert_detailitem_code(rec.detail)
            
            for idx in range(len(rec.locations)):
                loc = self.convert_locationitem_code(rec.locations[idx])
                item.locations[idx] = loc

            for idx in range(len(rec.descs)):
                desc = self.convert_descriptionitem_code(rec.descs[idx])
                item.descs[idx] = desc

            print(item.to_string())
            self.operations.append(item)

    # Extract Recording Item for Operation History
    def extract_operation_history(self):
        recs = get_recording_items(self.xls, 'Operation History')
        for rec in  recs:
            item = RecordingItemCode()
            item.major = self.convert_majoritem_code(rec.major)
            item.sub = self.convert_subitem_code(rec.sub)
            item.detail = self.convert_detailitem_code(rec.detail)
            
            for idx in range(len(rec.locations)):
                loc = self.convert_locationitem_code(rec.locations[idx])
                item.locations[idx] = loc

            for idx in range(len(rec.descs)):
                desc = self.convert_descriptionitem_code(rec.descs[idx])
                item.descs[idx] = desc

            print(item.to_string())
            self.operation_historys.append(item)

