import sqlite3
import time
import random
t0 = time.time()
data = []
for rw in range(1000000):
    data.append((random.random() * 10.0, 
                 time.time(),
                 random.randrange(1,4000)))
print(time.time() - t0, len(data))

with sqlite3.connect('oper.db') as conn:
    cursor = conn.cursor()
    sql = "UPDATE float_val SET val = ?, tstamp = ? WHERE id = ? "
    t0 = time.time()
    cursor.executemany(sql, data)
    conn.commit()
    print(time.time() - t0, len(data))