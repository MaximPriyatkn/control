import socket
import time
import threading
import pickle
import random
import sqlite3


def session(conn):
    c = 0
    while c < 300000:
        data = []
        for n in range(30):
            data.append((n, random.random()*10, time.time()))
        c += 30
        x = pickle.dumps(data)
        conn.send(x)
    print (c)

def manual(conn):
    while True:
        print('input data')
        n = int(input())
        v = float(input())
        data = []
        data.append((n, v, time.time()))
        x = pickle.dumps(data)
        conn.send(x)

# отправка данных по изменению в сервере
def getVal(sock):
    while True:
        time.sleep(5)
        data = [1, 1, 1]
        sock.send(pickle.dumps(data))
        print('get')
    return

# запись данных в сервер
def setVal(sock):
    while True:
        data = sock.recv(1024)
        try:
            id = pickle.loads(data)
            id = int(id)
        except:
            print('не id')
            continue
        with sqlite3.connect('sim.db') as conn:
            cursor = conn.cursor()
            sql = f'SELECT * FROM val WHERE id = {id}'
            cursor.execute(sql)
            res = cursor.fetchall()
            print(res)
    return


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('',8080))
sock.listen(5)
print('server running')
while True:
    conn, addr = sock.accept()
    print('connected', addr)
    th = threading.Thread(target = setVal, args=((conn,)))
    th1 = threading.Thread(target = getVal, args=((conn,)))
    th1.start()
    th.start()



conn.close()