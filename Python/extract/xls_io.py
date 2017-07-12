# -*- utf-8 -*-

import xlrd
import os.path

#　エクセルを開く
def open_xls(file_pass):
    xls = xlrd.Book()
    if os.path.exists(file_pass):
        xls = xlrd.open_workbook(file_pass)
        return [True, xls]

    return [False, xls]

