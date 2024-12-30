import socket
import datetime
import struct
from threading import Thread

IEC_IP = 'localhost'
IEC_PORT = 2400
IEC_BUFFER = 1024

# Получить адрес
def get_addr(addr):
    return list(addr)

# Получить значение с плавающей точкой
def get_float(val):
    res = str(struct.unpack('f', val)[0]) 
    return res

def send_command(kp):
    while True:
        cmd = [104, 14, 0, 0, 0, 0, 45, 1, 6, 0, 1, 2, 5, 4, 3, 0]
        tr = [104, 18, 2, 0, 0, 0, 50, 1, 6, 0, 5, 6, 2, 3, 4, 46, 182, 162, 200, 0]
        tu = input('введите значение')
        cmd[15] = int(tu)
        kp.send(bytes(cmd))
        print(bytes(cmd))


# Получить время из cp56
def get_time_cp56(cp56):
    d = list(cp56)
    s = d[1]<<8
    s = s + d[0]
    try:
        f=datetime.datetime(d[6] + 2000, d[5], d[4], d[3], d[2], s//1000, s%1000*1000)
    except:
        print("ошибка. во время передачи ", d)
        f = ''
    return f

# Разбить пакет на части по типам кадрам
def split_pack(frm):
    frm = list(frm)
    start_idx = 0
    len_pack = 0
    out = ''
    while True:
        if start_idx + 1 > len(frm):
            break
        len_pack = frm[start_idx + 1]
        end_idx = start_idx + len_pack + 2
        res = frm[start_idx:end_idx]
        if len(res) > 6:
            out += func[res[6]](bytes(res))
        start_idx = end_idx
    return out

def iec30(frm):
    addrh_start = 10
    addrh_end = 12
    addr_start = 12
    addr_end = 15
    val_start = 15
    date_start = 16
    date_end = 23
    out = ''
    pack_len = 11
    shift = 0
    addrh = get_addr(frm[addrh_start:addrh_end])
    while True:
        addr = get_addr(frm[addr_start + shift:addr_end + shift])
        value = frm[val_start + shift]
        inv = ''
        date = get_time_cp56(frm[date_start + shift: date_end + shift])
        out += f'{addrh}.{addr}\t{value}\t{inv}\t{date}\n'
        shift = shift + pack_len
        if addr_start + shift >= len(frm):
            break
    return out

def iec36(frm):
    addrh_start = 10
    addrh_end = 12
    addr_start = 12
    addr_end = 15
    val_start = 15
    val_end = 19
    inv_start = 19
    date_start = 20
    date_end = 27
    out = ''
    pack_len = 15
    shift = 0
    addrh = get_addr(frm[addrh_start:addrh_end])
    while True:
        addr = get_addr(frm[addr_start + shift:addr_end + shift])
        value = get_float(frm[val_start + shift:val_end+shift])
        inv = frm[inv_start + shift]
        date = get_time_cp56(frm[date_start + shift: date_end + shift])
        out += f'{addrh}.{addr}\t{value}\t{inv}\t{date}\n'
        shift = shift + pack_len
        if addr_start + shift >= len(frm):
            break
    return out

func = [0]*255
func[30] = iec30
func[36] = iec36

# Подключиться
kp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
kp.connect((IEC_IP,IEC_PORT))
tu = Thread(target=send_command, args=(kp,))
tu.start()
pack_init = bytes((104, 4, 7, 0, 0, 0))
pack_ack = pack_init
print('connect')
with open('log.txt', 'a+') as f_log:
    while True:
        kp.send(pack_ack)
        frm = kp.recv(IEC_BUFFER)
        pack_ack = frm 
        out = split_pack(frm)
        if out != '':
            f_log.write(out)
            f_log.flush()
