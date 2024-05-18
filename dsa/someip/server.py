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
        self.sock.bind(('192.168.1.6',30491))

    def send(self, data: bytes, ip_addr: str, port):
        self.sock.sendto(data, (ip_addr, int(port)))


if __name__ == '__main__':
    from dsa.someip.payload import BaseDataPayload,SomeIpPacket

    client = UdpClient()
    payload='zhangxinbo'.encode('utf-8')
    packet=SomeIpPacket('0x1234','0x5678',
                        '0x9012','0x3456',
                        '0x12','0x34',SomeIpPacket.MessageType.REQUEST,SomeIpPacket.ReturnCode.E_OK,
                        payload)
    print(bytes(packet))
    client.send(bytes(packet), '192.168.1.6', 30501)
