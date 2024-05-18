import socket


class UdpServer:
    def __init__(self, ip_addr: str, port):
        self.ip_addr = ip_addr
        self.port = int(port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip_addr, self.port))

    def run(self):
        while True:
            data, ip_port = self.sock.recvfrom(1024)
            print(data, ip_port)


class UdpClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, data: bytes, ip_addr: str, port):
        self.sock.sendto(data, (ip_addr, int(port)))


if __name__ == '__main__':
    server=UdpServer('192.168.1.6',30501)
    server.run()