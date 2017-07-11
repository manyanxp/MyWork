# -*- coding: utf-8 -*-

import cx_Oracle
import os

def execute()

def main():
    constr = "User ID=kyosan_db; Password=Orlando_DB0; Data Source=OrlandoDB;DBA privilege=SYSDBA"
    con = cx_Oracle.connect('kyosan_db', 'Orlando_DB0', 'localhost/OrlandoDB')
    cur = con.cursor()
    sql = 'select * from t_alarm where occurred_time >= TO_DATE(\'2017/05/01 00:00:00\', \'YYYY-MM-DD HH24:MI:SS\') order by occurred_time'
    cur.execute(sql)
    rows = cur.fetchall()

    for row in rows:
        seq_no = row[0]
        ats_device_id = row[1]
        seq_time = row[2]
        occurred_time = row[3]
        print(str(seq_no) + ',' + str(ats_device_id) + "," + occurred_time.strftime('%Y/%m/%d %H:%M:%S'))

    cur.close()


if __name__ == '__main__':
    os.environ["NLS_LANG"] = "JAPANESE_JAPAN.AL32UTF8"
    main()
