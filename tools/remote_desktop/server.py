import concurrent.futures
import io
import socket
import struct
import time

from screeninfo import get_monitors
from mss import mss
from mss.tools import to_png

import pickle


class Server:
    def __init__(self):
        self.pools = concurrent.futures.ThreadPoolExecutor(10)
        self.monitors = get_monitors()

    def send_screens_info(self,client_sock: socket.socket):
        while True:
            bio = io.BytesIO()
            for m in self.monitors:
                monitor = {
                    "left": m.x,
                    "top": m.y,
                    "width": m.width,
                    "height": m.height
                }

                # 使用mss截图
                with mss() as sct:
                    sct_img = sct.grab(monitor)
                    dt = to_png(sct_img.rgb, sct_img.size)
                    # to_png(sct_img.rgb, sct_img.size,output=rf'e:\sss\s{time.time()}.png')
                    pickle.dump(dt, bio)

            bio.seek(0)
            data = bio.read()
            client_sock.sendall(struct.pack('<i', len(data)) + data)
            print('已发送',client_sock)
            time.sleep(0.001)
            # break

    def handle_client_input(self, client_sock: socket.socket, client_addr):
        input_bytes = client_sock.recv(1024)

    def start(self, port: int):
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.bind(('0.0.0.0', port))

        server_sock.listen()

        while True:
            client_sock, client_addr = server_sock.accept()

            print('新的客户已接入', client_addr)
            self.pools.submit(self.send_screens_info,client_sock)


if __name__ == '__main__':
    s = Server()
    s.start(5900)
    # s.send_screens_info(1)
