import sqlite3
import shlex
import argparse
import re
import time, random

DB_CONF = "../db_conf/conf.db"
DB_OPER = "../db_oper/oper.db"

def set_sim_data():
    id = get_list_id(DB_OPER, 'value')
    data = []
    for row in id:
        data.append((random.random() * 10, time.time(), row))
    with sqlite3.connect(DB_OPER) as conn:
        cursor = conn.cursor()
        sql = "UPDATE value SET val=?, tstamp=? WHERE id=?"
        cursor.executemany(sql, data)
        conn.commit()


def get_list_id(bd, tab):
    id = []
    with sqlite3.connect(bd) as conn:
        cursor = conn.cursor()
        sql = f'SELECT id FROM {tab}'
        cursor.execute(sql)
        id_in = cursor.fetchall()
        for id_ in id_in:
            id.append(id_[0])
    return id

def update_id_oper():
    id_new = get_list_id(DB_CONF, 'conf')
    id_old = get_list_id(DB_OPER, 'value')
    id_remove = []
    id_add = []
    cnt_add = len(id_new)
    cnt_remove = 0
    for id in id_old:
        try:
            index = id_new.index(id)
            id_new.pop(index)
            cnt_add -= 1
        except:
            id_remove.append((id,))
            cnt_remove += 1
    for row in id_new:
        id_add.append((row,))

    with sqlite3.connect(DB_OPER) as conn:
        cursor = conn.cursor()
        sql = 'INSERT INTO value VALUES (?, NULL, NULL)'
        cursor.executemany(sql, id_add )
        conn.commit()
        sql = 'DELETE FROM value WHERE id = ?'
        cursor.executemany(sql, id_remove )
        conn.commit()
    print(f'add {cnt_add}, remove {cnt_remove}')

# Получить значения по имени сигнала
def get_value(filt):
    data = []
    print(filt)
    with sqlite3.connect(DB_CONF) as conn:
        cursor = conn.cursor()
        for cflt in filt:
            sql = f'''SELECT id FROM conf
                        WHERE conf.name LIKE "{cflt}"
            '''
            cursor.execute(sql)
            data.extend(cursor.fetchall())
    id = []
    for row in data:
        id.append(str(row[0]))
    id = ",".join(id)
    data = []
    with sqlite3.connect(DB_OPER) as conn:
        cursor = conn.cursor()
        sql = f'''SELECT val, tstamp FROM value
                  WHERE value.id IN ({id})
            '''
        print(sql)
        cursor.execute(sql)
        data.extend(cursor.fetchall())
    print(data)

# Получить идентификаторы сигналов
def get_id(filt):
    data = []
    print(filt)
    with sqlite3.connect(DB_CONF) as conn:
        cursor = conn.cursor()
        for cflt in filt:
            sql = f'''SELECT * FROM conf
                        LEFT JOIN conf_iec
                        ON conf_iec.id = conf.id
                        WHERE conf.name LIKE "{cflt}"
            '''
            cursor.execute(sql)
            data.extend(cursor.fetchall())
    for row in data:
        print(row)

func = {'get_id':get_id, 'get_value':get_value}

def main():
    cmd = ''
    while True:
        cmd = input("command? ")
        if cmd == 'quit':
            break
        try:
            cmd_func = re.search(r'.*\(', cmd).group()[:-1]
            cmd_param = re.search(r'\(.*\)',cmd).group()
            if len(cmd_param) > 2:
                cmd_param = cmd_param.replace('*','%')
                cmd_param = cmd_param.replace(' ','')
                cmd_param = cmd_param[1:-1].split(',')
            else:
                quit()
            if cmd_func in func:
                func[cmd_func](cmd_param)
        except:
            print('не верные параметры')

if __name__ == '__main__':
    #main()
    #update_id_oper()
    set_sim_data()