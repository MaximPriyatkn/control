
import datetime
from datetime import datetime
import socket
import pickle

lim = [4.5,6.0,12.4,16.0]
alm = ['Давление ниже аварийного', 'Давление ниже предельного', 'Норма', 'Давление выше предельного', 'Давление выше аварийного']
cur = ''

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 8080))

n = 0

while True:
    data = sock.recv(676)
    print(len(data))
    inp = pickle.loads(data)

    for s in inp:
        n += 1
        val = s[1]
        tme = datetime.fromtimestamp(s[2]).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        cnt_lim = len(lim) - 1
        msg = ''
        for i in range(cnt_lim):
            if val < lim[i]:
                if cur != alm[i]:
                    msg = (tme,str(val), alm[i])
                    cur = alm[i]
                break
        if val > lim[cnt_lim]:
            if cur != alm[i]:
                msg = (tme,str(val), alm[cnt_lim])        
                cur = alm[i]
        if n%10000 == 0:
            print (tme)
            
    if msg != '':
        print(msg)
    print('-------------------------------\n')

print('\n', time.time() - t0)