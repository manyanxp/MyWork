# -*- utf-8 -*-
#-----------------------------------------------------------------------------
# 自作ライブラリパス追加
import sys,os
print(os.path.dirname(os.path.abspath(__file__)) + '/../mylibpy')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../mylibpy')
#-----------------------------------------------------------------------------

from create_query import CreateQuerysForAtsAlarm as cqfatsa
from extract_recording_item import ExtractRecrodingItem
from diagnostics import  stopwatch

if __name__ == '__main__':
    proc = ExtractRecrodingItem('test.xls')
    proc.extract_ats_alarm()
    proc.extract_train_alarm()
    proc.extract_others_alarm()
    proc.extract_operation()
    proc.extract_operation_history()

    sw = stopwatch.Stopwatch()
    sw.start()
    make = cqfatsa(proc.ats_alarms)
    querys = make.insert_alarm_query()

    f = open('insert_ats_alarm.txt','a')
    for query in querys:
        f.write(query + ';\n')

    f.close()
    sw.end()
    print('処理時間:{0:f}'.format(sw.elapsed_time))

    sw = stopwatch.Stopwatch()
    sw.start()
    make = cqfatsa(proc.train_alarms)
    querys = make.insert_alarm_query()

    f = open('insert_train_alarm.txt','a')
    for query in querys:
        f.write(query + ';\n')

    f.close()
    sw.end()
    print('処理時間:{0:f}'.format(sw.elapsed_time))

    sw = stopwatch.Stopwatch()
    sw.start()
    make = cqfatsa(proc.others_alarms)
    querys = make.insert_alarm_query()

    f = open('insert_others_alarm.txt','a')
    for query in querys:
        f.write(query + ';\n')

    f.close()
    sw.end()
    print('処理時間:{0:f}'.format(sw.elapsed_time))
