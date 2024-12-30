import socket
IEC_IP = 'localhost'
IEC_PORT = 2400


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('',2404))
sock.listen(5)
print('server running')
kp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
kp.connect((IEC_IP,IEC_PORT))
pu, addr = sock.accept()
print('connected', addr)

while True:
    frm = pu.recv(1024)
    print('from pu', list(frm))
    kp.send(frm)
    frm = kp.recv(1024)
    pu.send(frm)
    print('from kp', list(frm))
