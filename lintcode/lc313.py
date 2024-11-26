import queue
import time

import pyodbc
from typing import List


class AccessdbAgent:
    queue=queue.Queue(1)
    queue.put(1)

    def __init__(self, accessdb_file_path: str):
        self.conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + accessdb_file_path + ';'
        self.conn=None

    def __enter__(self):
        self.conn=pyodbc.connect(self.conn_str)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        pass

    def get_data(self, sql: str):
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def exec(self, sqls: List[str]):
        self.queue.get()
        # self.queue.get()
        # print(self.queue.qsize())
        try:

            # print(rf'{sqls}进来了')
            with self.conn.cursor() as cursor:
                for sql in sqls:
                    cursor.execute(sql)
                cursor.commit()
            pass
        finally:
            self.queue.put(1)
            pass


def fff(aa, bb,agent=AccessdbAgent(r"D:\shici\bbb.accdb")):
    sql = f"insert into table1(aa,bb) values({aa},'{bb}')"
    agent.exec([sql])



st=time.time()

from concurrent.futures.thread import ThreadPoolExecutor

pool = ThreadPoolExecutor(100000)

res = []

agent=AccessdbAgent(r"D:\shici\bbb.accdb")
with agent:
    for i in range(10000):
        res.append(pool.submit(fff, i + round(time.time()), str(i) * 3,agent))
        # time.sleep(0.1)

    pool.shutdown()
    #
for r in res:
    r.result()


print(time.time()-st)

