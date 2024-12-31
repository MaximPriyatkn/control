import sqlite3
import time

class ScODB:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        sql = 'CREATE TABLE IF NOT EXISTS val (id PRIMARY KEY, kp INTEGER, addr INTEGER, value FLOAT, tstamp FLOAT)'
        self.cursor.execute(sql)
    def insert(self, new_value):
        sql = 'INSERT INTO val VALUES (?,?,?,?,?)'
        self.cursor.executemany(sql, new_value)
        self.conn.commit()
    def update(self, new_value):
        sql = 'UPDATE val SET value = ?, tstamp = ? WHERE id = ?'
        data = []
        for n, row in enumerate(new_value):
            data.append((row[3], row[4], row[0]))
        self.cursor.executemany(sql, data)
        self.conn.commit()
    def get_config(self):
        sql = "SELECT id, type, ha, la FROM conf_iec"
        data = {}
        self.cursor.execute(sql)
        config = self.cursor.fetchall()
        for rw in config:
            if rw[1] not in data:
                data[rw[1]] = {}
            if rw[2] not in data[rw[1]]:
                data[rw[1]][rw[2]] = {}
            if rw[3] not in data[rw[1]][rw[2]]:
                data[rw[1]][rw[2]][rw[3]] = rw[0]
        return data

a = ScODB('oper.db')
new_value =  (
    (1,0,0,1.0,345.0),(2,0,0,3.4,335.0),(3,0,0,2.1,245.1),(4,0,0,2.2,135.1)
)
#a.insert(new_value)
#a.update(new_value)

d = a.get_config()   
t0 = time.time()
print(d[36][515][197642])
print(time.time() - t0)