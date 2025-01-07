import sys
import json
import socket
import time, datetime
import threading
import struct
import sqlite3
from iec_60870 import *


is_conn = False


def get_buffer():
    with sqlite3.connect('oper.db') as conn:
        cursor = conn.cursor()
        sql = "SELECT ha, la, val, tstamp FROM out_buffer WHERE val not NULL ORDER BY ID LIMIT 10"
        cursor.execute(sql)
        data = cursor.fetchall()
    for row in data:
        frm = list(struct.pack('i', row[0])[0:2])
        frm.extend(list(struct.pack('i', row[1])[0:3]))
        frm.extend(list(struct.pack('f', row[2])))
        frm.append(0) 
        ts = datetime.datetime.now()
        s = ts.second * 1000 + ts.microsecond // 1000
        frm.extend(list(struct.pack('i', s))[0:2])
        frm.extend((ts.minute, ts.hour,ts.day,ts.month,ts.year - 2000))  
    return frm

def send_data(pu):
        n = 0
        while True:
            time.sleep(5)
            data = [104, 25, 0, 0, 0, 0, 36, 1, 3, 0]
            data[2] = n
            data.extend(get_buffer())
            pu.send(bytes(data))
            n += 2
            if n > 250:
                n = 0



def run_test(pu):
    print('run test')
    is_run = True
    while True:
        frm = pu.recv(1024)
        if frm == 'b':
            break
        print (list(frm))
        if frm == FRM_START_ACT:
            print ('--->', FRM_START_CON)
            pu.send(FRM_START_CON)
        elif frm == FRM_TST_ACT:
            print ('--->', FRM_TST_CON)
            pu.send(FRM_TST_CON)
        print('-->', FRM_ACK)
        pu.send(FRM_ACK)
        if is_run:    
            th = threading.Thread(target=send_data, args=(pu,))
            th.start()
            is_run = False  
        

def init_server(conf, sock):
    sock.bind((conf['IP'],conf['PORT']))
    sock.listen(conf['CONN'])
    print('server running')
    th = []
    while True:
        pu, addr = sock.accept()
        print('client connected', addr)
        th = threading.Thread(target=run_test, args=(pu,))
        th.start()
      
def init_client(conf):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    outlog(f'Start client {conf}', 1)
    global is_conn
    while True:
        try:
            if not is_conn:
                sock.connect((conf['IP'],conf['PORT']))
                sock.send(FRM_START_ACT)
                outlog(f'pu -> kp {list(FRM_START_ACT)}') 
                outlog('Wait answer from server(KP)')
                cnt = [10,0]
            frm = sock.recv(IEC_BUFFER)
            if frm == b'':
                outlog('Disconnect', 2)
                raise Exception() 
            s_frm = split_frm(frm)
            for n, apdu in enumerate(s_frm):
                outlog(f'pu <- kp{list(apdu)}')
                if apdu == FRM_START_CON:
                    outlog('Connect',1)
                    is_conn = True
                    th_rcv = threading.Thread(target=send_client, args=(sock,))
                    th_rcv.start()
                    th_que = threading.Thread(target=get_queue_recv)
                    th_que.start()
                    th_db = threading.Thread(target=read_db)
                    th_db.start()
                elif len(apdu) > 6 and apdu[6] == 100:
                    if n == 0: 
                        sock.send(bytes([104, 4, 1, 0, 10, 0]))
                        sock.send(FRM_TST_ACT)
                        outlog(f'pu -> kp{list([104, 4, 1, 0, 10, 0])}') 
                        outlog(f'pu -> kp{list(FRM_TST_ACT)}')     
                elif apdu == FRM_TST_ACT:
                    sock.send(FRM_TST_CON)
                    outlog(f'pu -> kp{list(FRM_TST_CON)}')
                elif apdu == FRM_TST_CON:
                    pass
                else:
                    cnt = [None, None]
                    if n == len(s_frm) - 1:
                       cnt = [apdu[2],apdu[3]]
                    if len(apdu) > 6:
                        recv_client(sock, apdu, cnt)
        except Exception as e:
            print (e, cnt, apdu)
            is_conn = False
            q_recv.empty()
            outlog(f"No connect, wait {conf['TIMEOUT']}s",1)
            time.sleep(conf['TIMEOUT'])    
            sock.close()
            init_client(conf)

def get_queue_recv():
    while is_conn:
        while not q_recv.empty():
            frm = q_recv.get()
            try:
                for val in asdu_unpack[frm[6]](frm):   
                    q_out.put(val)
            except Exception as e:
                print(e)
                print(list(frm))
        if not q_out.empty():
            flush_buffer()
        time.sleep(0.001)
 

def send_client(sock):
    while is_conn:
        while not q_out.empty():
            frm = q_out.get()
            sock.send(bytes(frm))
        time.sleep(0.001)


def recv_client(sock, asdu, cnt):
    q_recv.put(asdu)
    if cnt[0] == None:
        return
    if cnt[0] >= 254:
        cnt[0] = 0
        cnt[1] += 1
    frm = [104, 4, 1, 0, cnt[0] + 2, cnt[1]]
    outlog(f'pu -> kp {frm}')
    sock.send(bytes(frm))





def init_drv(conf):
    if conf['CONN'] > 0:
        init_server(conf)
    else:
        init_client(conf)



def main(argv):
    outlog('Start driver',1)
    if len(argv) != 2:
        id_config = 'iec_1'
    else:
        id_config = argv[1]
    try:
        with open(CONF_FILE, 'r+') as fconf:
            conf = json.load(fconf)
            if id_config in conf:
                conf = conf[id_config]
            else:
                outlog(f'Not found key {id_config}',3)
    except:
        outlog("Error config file. Using default config for iec-master",2)
        conf = CONF_DEFAULT
    init_drv(conf)





if __name__ == '__main__':
    main(sys.argv)
    #get_buffer()

