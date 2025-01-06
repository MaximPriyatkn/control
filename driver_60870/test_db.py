import sqlite3
import time
from sys import stdin
import datetime
import struct

def select():
    with sqlite3.connect('oper.db') as conn:
        cursor = conn.cursor()
        sql = "SELECT * FROM out_buffer WHERE tstamp > ? LIMIT 100"
        while True:
            t0 = time.perf_counter()
            ts = (5.0,)
            cursor.execute(sql,ts)
            data = cursor.fetchall()
            t1 = time.perf_counter() - t0
            if  t1 > 0.03:
                print("time", t1, len(data))
            time.sleep(0.05)

def input_data():
    lines = []
    for line in stdin:
        lines.append(line)
    print (lines)

def get_buffer():
    with sqlite3.connect('oper.db') as conn:
        cursor = conn.cursor()
        sql = "SELECT ha, la, val, tstamp FROM out_buffer WHERE val not NULL ORDER BY ID LIMIT 5"
        cursor.execute(sql)
        data = cursor.fetchall()
    cnt, len_pack = 0, 0
    frm = []    
    for row in data:
        frm.extend(list(struct.pack('i', row[0])[0:2]))
        frm.extend(list(struct.pack('i', row[1])[0:3]))
        frm.extend(list(struct.pack('f', row[2])))
        frm.append(0) 
        ts = datetime.datetime.now()
        s = ts.second * 1000 + ts.microsecond // 1000
        frm.extend(list(struct.pack('i', s))[0:2])
        frm.extend((ts.minute, ts.hour,ts.day,ts.month,ts.year - 2000)) 
        if cnt == 0:
            len_pack = len(frm)
        cnt += len_pack 
    return cnt, frm

cnt, data = get_buffer()
print(cnt, data.__sizeof__() )