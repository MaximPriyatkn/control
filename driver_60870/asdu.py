import time
import datetime
import struct
IEC_DELTA_TIME = 0.01
out_cnt = [0,0]
in_cnt = [0,0]

#Увеличить счетчик отправленных сигналов
def inc_cnt(cnt):
    if cnt[0] > 252:
        cnt[0] = 0
        cnt[1] += 1
        if cnt[1] > 254:
            cnt[1] = 0
    else:
        cnt[0] += 2
    


# Получить время из cp56
def get_time_cp56(cp56):
    d = list(cp56)
    s = d[1]<<8
    s = s + d[0]
    fs = None
    try:
        f=datetime.datetime(d[6] + 2000, d[5], d[4], d[3], d[2], s//1000, s%1000*1000).timestamp()
        t0 = time.time()
        if f < t0 - IEC_DELTA_TIME or f > t0 + IEC_DELTA_TIME:
            fs = f-time.time()
    except:
        print("ошибка. во время передачи ", d)
        f = 0.0
    return f, fs

# Получить значение с плавающей точкой
def get_float(val):
    res = struct.unpack('f', val)[0] 
    return res

# Получить адрес
def get_addr(addr):
    res = 0
    if len(addr) == 3:
        res = addr[0] + (addr[1]<<8) + (addr[2]<<16)
    if len(addr) == 2:
        res = addr[0] + (addr[1]<<8)
    return int(res)

def asdu_from_36(frm):
    s_ix = 12
    len_frm = 15
    res = []
    caddr = get_addr(frm[s_ix-2:s_ix])
    while s_ix < len(frm) - 7:
        iaddr = get_addr(frm[s_ix:s_ix+3])
        val = get_float(frm[s_ix+3:s_ix+7])
        inv = frm[s_ix+7]
        ts, ts2 = get_time_cp56(frm[s_ix+8:s_ix+15])
        s_ix += len_frm
        res.append((caddr, iaddr, val, inv, ts, ts2))
    return res

def asdu_to_45(caddr, iaddr, value):
    res = [104, 14, out_cnt[0], out_cnt[1], 0, 0, 45]
    cot = [1,6,0]
    caddr_frm = struct.pack('>i', caddr)[2:]
    iaddr_frm = struct.pack('>i', iaddr)[1:]
    res.extend(cot)
    res.extend(caddr_frm)
    res.extend(iaddr_frm)
    res.append(value)
    inc_cnt(out_cnt)
    return res

asdu_pack = {
    45: asdu_to_45
    }



asdu_unpack = {
    36: asdu_from_36
    }


if __name__ == '__main__':
    frm = [104, 100, 182, 0, 0, 0, 36, 6, 3, 0, 2, 1, 0, 0, 1, 88, 57, 48, 65, 0, 173, 90, 30, 20, 5, 1, 25, 0, 0, 2, 109, 231, 107, 65, 0, 173, 90, 30, 20, 5, 1, 25, 0, 0, 3, 143, 194, 213, 63, 0, 173, 90, 30, 20, 5, 1, 25, 0, 0, 4, 6
    , 129, 117, 64, 0, 173, 90, 30, 20, 5, 1, 25, 0, 0, 5, 195, 245, 188, 65, 0, 173, 90, 30, 20, 5, 1, 25, 0, 0, 6, 49, 8, 203, 65, 81, 173, 90, 30, 20, 5, 1, 25]
    #print(asdu_36(bytes(frm)))
    tu = [104, 14, 0, 0, 0, 0, 45, 1, 6, 0, 1, 2, 5, 4, 3, 0]
    print(asdu_to_45(258, 2230, 1))
    tr = [104, 18, 2, 0, 0, 0, 50, 1, 6, 0, 5, 6, 2, 3, 4, 46, 182, 162, 200, 0]
    print(asdu_to_45(258, 2230, 1))
