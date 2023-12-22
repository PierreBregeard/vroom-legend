from .Socket import Socket


class Client(Socket):

    def __init__(self, ip, port):
        super().__init__()
        self.sock.connect((ip, port))

    def receive(self):
        # data = self.sock.recvfrom(1024)
        # if not data:
        #     return None
        # size = int(data[:8].decode())

        # data = b""
        # while size != 0:
        #     res = self.sock.recvfrom(min(1024, size))
        #     size -= len(res)
        #     data += res
        # return data

        data = self.sock.recvfrom(1024)
        return data

    def send(self, data):
        self.sock.send(data)
