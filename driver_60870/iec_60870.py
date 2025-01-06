import logging
import queue
import time
from asdu import *

FRM_START_ACT = bytes([104, 4, 7, 0, 0, 0])
FRM_START_CON = bytes([104, 4, 11, 0, 0, 0])
FRM_STOP_ACT = bytes([104, 4, 37, 0, 0, 0])
FRM_STOP_CON = bytes([104, 4, 17, 0, 0, 0])
FRM_TST_ACT = bytes([104, 4, 67, 0, 0, 0])
FRM_TST_CON = bytes([104, 4, 131, 0, 0, 0])
FRM_ACK = bytes([104, 4, 1, 0, 0, 0])
FRM_ACK_GQ = bytes([104, 4, 1, 0, 6, 0])
IEC_BUFFER = 1024
CONF_FILE = 'iec.json'
LOG_FILE = 'iec.log'
CONF_DEFAULT = {"IP":"192.168.2.52",
                        "PORT":2400,
                        "CONN":0,
                        "TIMEOUT":10}
PRINT_LVL = 1

q_recv = queue.Queue()
q_out = queue.Queue()


log = logging.getLogger(__name__)
logging.basicConfig(
    level = logging.ERROR,
    filename=LOG_FILE,
    filemode='a',
    format="%(asctime)s %(levelname)s %(message)s"
)

def outlog(msg, lvl = 0, is_print = True):
    if lvl == 2: log.warning(msg)
    elif lvl == 4: log.critical(msg)
    elif lvl == 1: log.info(msg)
    elif lvl == 3: log.error(msg)
    else: log.debug(msg)
    if PRINT_LVL <= lvl and is_print:
        print(f'IEC_driver --> {msg}')

def split_frm(frm):
    s_ix, e_ix, res = 0, 0, []
    while s_ix < len(frm) - 2:
        if frm[s_ix] != 104:
            break
        e_ix = frm[s_ix + 1] + s_ix + 1
        res.append(frm[s_ix: e_ix+1])
        s_ix = e_ix+1
    return res


def flush_buffer():
    with open('buffer.log', 'a+') as flog:
        while not q_out.empty():
            flog.write(f'{q_out.get()}\n')
    
  







if __name__ == "__main__":
    frm = bytes([104, 25, 8, 1, 0, 0, 36, 1, 3, 0, 3, 2, 10, 4, 3, 16, 88, 162, 65, 0, 164, 209, 5, 16, 5, 1, 25, 104, 100, 10, 1, 0, 0, 36, 6, 3, 0, 2, 1, 0, 0, 1, 172, 28, 181, 65, 0, 164, 209, 5, 16, 5, 1, 25, 0, 0, 2, 68, 139, 216,
65, 0, 164, 209, 5, 16, 5, 1, 25, 0, 0, 3, 39, 177, 1, 66, 0, 164, 209, 5, 16, 5, 1, 25, 0, 0, 4, 47, 221, 100, 65, 0, 164, 209, 5, 16, 5, 1, 25, 0, 0, 5, 221, 36, 223, 65, 0, 164, 209, 5, 16, 5, 1, 25, 0, 0, 6, 250, 126, 142
, 64, 81, 164, 209, 5, 16, 5, 1, 25, 104, 40, 12, 1, 0, 0, 36, 2, 3, 0, 2, 1, 7, 4, 3, 139, 108, 211, 65, 0, 168, 209, 5, 16, 5, 1, 25, 9, 4, 3, 248, 83, 225, 65, 0, 168, 209, 5, 16, 5, 1, 25, 104, 25, 14, 1, 0, 0, 36, 1, 3,
0, 3, 2, 10, 4, 3, 145, 237, 30, 65, 0, 168, 209, 5, 16, 5, 1, 25, 104, 100, 16, 1, 0, 0, 36, 6, 3, 0, 2, 1, 0, 0, 1, 127, 106, 70, 65, 0, 168, 209, 5, 16, 5, 1, 25, 0, 0, 2, 39, 49, 131, 65, 0, 168, 209, 5, 16, 5, 1, 25, 0,
0, 3, 49, 8, 234, 65, 0, 168, 209, 5, 16, 5, 1, 25, 0, 0, 4, 231, 251, 139, 65, 0, 168, 209, 5, 16, 5, 1, 25, 0, 0, 5, 27, 47, 69, 65, 0, 168, 209, 5, 16, 5, 1, 25, 0, 0, 6, 164, 112, 77, 65, 81, 168, 209, 5, 16, 5, 1, 25])
    print(list(frm))
    for f in split_frm(frm):
        print(list(f))