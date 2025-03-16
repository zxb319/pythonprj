import io
import pickle
import socket
import struct
import threading
import time

from PIL import ImageTk, Image


class Client:
    """
    张新波 时代sdsdsssssddss
    asdadadasdasdasda
    asd
    asd
    fd
    df
    df
    df
    df

    """
    def __init__(self):
        pass

    def connect(self, ip_addr, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip_addr, port))
        return sock

    def receive_screens_info(self, sock: socket.socket):
        bytes_data = sock.recv()

    def start(self, ip_addr, port):

        title = rf"远程桌面-{ip_addr}:{port}"

        import tkinter as tk
        from tkinter import ttk

        # 创建主窗口
        root = tk.Tk()
        root.title(title)
        root.geometry("1200x800")

        # 创建Notebook控件 ‌:ml-citation{ref="1,6" data="citationList"}
        notebook = ttk.Notebook(root)
        notebook.pack(fill='both', expand=True)

        sock = self.connect(ip_addr, port)

        def recv_all(sock, n):
            """接收指定长度的数据"""
            data = b''
            while len(data) < n:
                packet = sock.recv(n - len(data))
                if not packet:
                    return None
                data += packet
            return data

        def receive_screen_info():
            screen_data_list = []
            data_len = recv_all(sock, 4)
            l = struct.unpack('<i', data_len)[0]
            data = recv_all(sock, l)
            bio = io.BytesIO(data)
            while bio.tell() < len(data):
                cur = pickle.load(bio)
                screen_data_list.append(cur)

            labels = []
            for i, screen_data in enumerate(screen_data_list):
                tab = ttk.Frame(notebook)
                notebook.add(tab, text=rf"屏幕{i + 1}")

                panel = ttk.Label(tab)
                pil_image = Image.open(io.BytesIO(screen_data))
                pil_image.thumbnail((notebook.winfo_width(),notebook.winfo_height()))
                img = ImageTk.PhotoImage(pil_image)
                panel.image = img
                panel.pack(side="bottom", fill="both")
                labels.append(panel)

            while True:
                screen_data_list = []
                data_len = recv_all(sock, 4)
                data = recv_all(sock, struct.unpack('<i', data_len)[0])
                print(len(data)/1024//1024)
                bio = io.BytesIO(data)
                while bio.tell() < len(data):
                    cur = pickle.load(bio)
                    screen_data_list.append(cur)

                for i, screen_data in enumerate(screen_data_list):
                    panel = labels[i]
                    pil_image = Image.open(io.BytesIO(screen_data))
                    pil_image.thumbnail((notebook.winfo_width(),notebook.winfo_height()))
                    img = ImageTk.PhotoImage(pil_image)
                    panel.config(image=img)
                    panel.image = img

        t = threading.Thread(target=receive_screen_info)
        t.setDaemon(True)
        t.start()

        root.mainloop()


if __name__ == '__main__':
    c = Client()
    c.start('zxb-shinelon-m7', 5900)
    # c.connect('127.0.0.1',5900)
