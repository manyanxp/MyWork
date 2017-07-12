# -*- utf-8 -*-

from create_query import CreateQuerysForAtsAlarm as cqfatsa
from extract_recording_item import ExtractRecrodingItem

if __name__ == '__main__':
    proc = ExtractRecrodingItem('test.xls')
    proc.extract_ats_alarm()
    proc.extract_train_alarm()
    proc.extract_others_alarm()

    make = cqfatsa(proc.ats_alarms)
    querys = make.insert_alarm_query()

    f = open('insert_ats_alarm.txt','a')
    for query in querys:
        f.write(query + ';\n')

    f.close()

    make = cqfatsa(proc.train_alarms)
    querys = make.insert_alarm_query()

    f = open('insert_train_alarm.txt','a')
    for query in querys:
        f.write(query + ';\n')

    f.close()

    make = cqfatsa(proc.others_alarms)
    querys = make.insert_alarm_query()

    f = open('insert_others_alarm.txt','a')
    for query in querys:
        f.write(query + ';\n')

    f.close()

