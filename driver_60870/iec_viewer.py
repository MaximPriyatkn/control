import socket
import threading
import time
IEC_IP = '192.168.2.52'
IEC_IP_SRV = ''
IEC_PORT = 2400
IEC_PORT_SRV = 2404

def kp_pu(kp, pu):
    while True:
        frm = pu.recv(1024)
        if frm == b'':
            kp.close()
            pu.close()
            break
        print('from pu = ', time.time(), list(frm))
        kp.send(frm)

def pu_kp(kp, pu):
    while True:
        frm = kp.recv(1024)
        if frm == b'':
            kp.close()
            pu.close()
            break
        print('from kp = ',time.time(),list(frm))
        pu.send(frm)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((IEC_IP_SRV,IEC_PORT_SRV))
sock.listen(5)
print('server running')
pu, addr = sock.accept()
print('connected', addr)

kp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
kp.connect((IEC_IP,IEC_PORT))


th = threading.Thread(target=kp_pu, args = (kp, pu))
th1 = threading.Thread(target=pu_kp, args = (kp, pu))
th.start()
time.sleep(1)
th1.start()
print(th, th1)