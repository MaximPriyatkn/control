import sqlite3
import random
import time
import csv

class Db:
    fname = 'c:/Users/LocalAdmin/prog/scada/control/data_simulator/sim.db'
    def create_db(self):
        with sqlite3.connect(self.fname) as conn:
            conn.execute('VACUUM')
            conn.commit()
            cursor = conn.cursor()
            # Таблица значений сигналов
            sql = 'CREATE TABLE IF NOT EXISTS val (id INTEGER PRIMARY KEY, float_v REAL, int_v INTEGER, ts_src FLOAT, ts FLOAT, inv INTEGER)'
            cursor.execute(sql)
            # Таблица алармов
            sql = 'CREATE TABLE IF NOT EXISTS alarm (ts_src FLOAT, ts FLOAT, signal TEXT, msg TEXT, ac INTEGER, lim INTEGER, partner FLOAT, inv INTEGER, direct INTEGER, ack_enable INTEGER, ack_user TEXT, ack_time FLOAT, src_srv TEXT, src_user TEXT, CONSTRAINT alarm_pk PRIMARY KEY (ts_src, signal))'
            cursor.execute(sql)
            # Таблица конфигурации типов сигналов
            sql = 'CREATE TABLE IF NOT EXISTS cfg_type_point (id INTEGER PRIMARY KEY, name TEXT, description TEXT)'
            cursor.execute(sql)
            # Таблица конфигурации свойств типов сигналов
            sql = 'CREATE TABLE IF NOT EXISTS cfg_prop_type (id INTEGER PRIMARY KEY, name TEXT, description TEXT, type_value INTEGER, type_point INTEGER, GRP INTEGER)'
            cursor.execute(sql)
            # Таблица точек
            sql = 'CREATE TABLE IF NOT EXISTS point (id INTEGER PRIMARY KEY, type_point INTEGER, name TEXT, description TEXT)'
            cursor.execute(sql)  
            # Таблица сигналов
            sql = 'CREATE TABLE IF NOT EXISTS signal (id INTEGER PRIMARY KEY, type_point INTEGER, prop_type INTEGER, name TEXT, description TEXT)'
            cursor.execute(sql)            
            conn.commit()
    # Модификация данных в таблице значений сигналов
    def set_test_data(self):
        with sqlite3.connect(self.fname) as conn:
            cursor = conn.cursor()
            sql = 'DELETE FROM val'
            cursor.execute(sql)
            sql = '''SELECT signal.id, cfg_prop_type.type_value FROM signal
                     JOIN cfg_prop_type
                     ON signal.prop_type = cfg_prop_type.id '''
            cursor.execute(sql)
            data = []
            id = 0
            for row in cursor.fetchall():
                v1 = None
                v2 = None
                inv = None
                if row[1] == 1:
                    v2 = random.randint(0,1)
                elif row[1] == 2:
                    v1 = random.random() * 10
                else:
                    v2 = random.randint(1,6)
                if random.random() < 0.1:
                    inv = 1
                data.append((id,v1, v2, time.time(),None,inv))
                id += 1
            sql = 'INSERT INTO val VALUES(?, ?, ?, ?, ?, ?)'
            cursor.executemany(sql, data)
            conn.commit()
    # Подготовка данных для имитиации значений сигналов        
    def sim_data(self, cnt=100, start_n=0):
        data = []
        for row in range(cnt):
            if row < cnt/5:
                v1 = random.random() * 10
                v2 = None
            elif row < cnt/1.5:
                v1 = None
                v2 = random.randint(0,5) 
            else:
                v1 = None
                v2 = random.randint(0,1)
            if random.random() < 0.1:
                inv = 1
            else:
                inv = None
            data.append((start_n, v1, v2, time.time(), None, inv))
            start_n += 1 
        return data
    # Обновление данных в таблице сигналов
    def update(self, data):
        with sqlite3.connect(self.fname) as conn:
            cursor = conn.cursor()
            sql = f'SELECT id, float_v, int_v FROM val WHERE id = {id}'
            cursor.execute(sql)
            cur = cursor.fetchone()
            if cur == None:
                print (f'! fault id = {id}')
                return 0
            print(data)
            sql = 'UPDATE val SET float_v = ?, int_v = ?, ts_src = ?, ts = ?,inv = ? WHERE id = ?'
            cursor.execute(sql, data)
            conn.commit()
    # Загрузка конфигурации сигналов
    def load_config(self):
        data = []
        with open('cfg_prop_type.tsv', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter='\t')
            for row in reader:
                data.append((
                    row['id'],
                    row['name'],
                    row['description'],
                    row['type_value'],
                    row['type_point'],
                    row['grp']

                ))
        with sqlite3.connect(self.fname) as conn:
            cursor = conn.cursor()
            sql = 'INSERT INTO cfg_prop_type VALUES (?,?,?,?,?,?)'
            cursor.executemany(sql, data)
    # Загрузка точек данных
    def load_point(self, cnt):
        data = []
        tp = 1
        for raw in range(cnt):
            data.append((raw, tp, 'ZDV_'+str(raw), "Задвижка_"+str(raw)))
        with sqlite3.connect(self.fname) as conn:
            cursor = conn.cursor()
            sql = 'INSERT INTO point VALUES (?, ?, ?, ?)'
            cursor.executemany(sql, data)
            conn.commit()        
    # Загрузка сигналов
    def load_signal(self):
        point = []
        data = []
        with sqlite3.connect(self.fname) as conn:
            cursor = conn.cursor()
            sql = "SELECT id, type_point FROM point"
            cursor.execute(sql)
            point = cursor.fetchall()
            cur_type = ''
            prop = []
            id = 0
            for p in point:
                if p[1] != cur_type:
                    cur_type = p[1]
                    sql = f'SELECT id FROM cfg_prop_type WHERE type_point = {cur_type}'
                    cursor.execute(sql)
                    prop = cursor.fetchall()
                for s in prop:
                    data.append((id, s[0], None, None, cur_type, p[0]))  
                    id += 1  
            sql = 'INSERT INTO signal VALUES (?,?,?,?,?,?)'
            cursor.executemany(sql, data)
            conn.commit()            
    
        



db = Db()
db.create_db()
#db.set_test_data()
#db.load_config()
#db.load_point(2000)
#db.load_signal()
while True:
    id = int(input('id = '))
    if id < 0:
        break
    v = input('value = ')
    float_v = None
    int_v = None
    inv = None
    try:
        int_v = int(v)
    except:
        try:
            float_v = float(v)
        except:
            continue    
    try:            
        inv = int(input('inv = '))
    except:
        inv = None

    db.update((float_v, int_v, time.time(), None, inv, id))