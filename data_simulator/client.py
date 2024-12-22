import datetime
from datetime import datetime
import socket
import pickle
import threading

def setVal(sock):
    while True:
        d = input('= ')
        sock.send(pickle.dumps(d))



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 8080))
th = threading.Thread(target=setVal, args=((sock,)))
th.start()
while True:
    data = sock.recv(676)
    print(pickle.loads(data))