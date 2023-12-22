import socket
from .Socket import Socket
import time


class Server(Socket):

    clients = {}
    tick = 10 / 1000  # tick rate for server response
    loopDelay = 0.1  # prevent big CPU usage

    @staticmethod
    def get_ipv4_address():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ipv4_address = s.getsockname()[0]
            s.close()
            return ipv4_address
        except socket.error as e:
            print("Error:", e)
            return None

    def __init__(self, ip, port):
        super().__init__()
        self.sock.bind((ip, port))
        self.sock.setblocking(False)

    def receive(self):
        try:
            data, client_address = self.sock.recvfrom(1024)
            if client_address not in self.clients:
                if len(self.clients) == 2:
                    self.send_to("Server is full", client_address)
                    return
                self.clients[client_address] = True
                print(f"New client connected: {client_address}")

            print(f"Received data from {client_address}: {data}")
            return data
        except socket.error as e:
            if e.errno in [10035, 11]:
                pass
            else:
                raise

    def listen(self):
        next_tick_time = time.time() + self.tick
        while True:
            data = self.receive()
            self.send_to_all(data)

            current_time = time.time()
            if current_time >= next_tick_time:
                next_tick_time = current_time + self.tick
            time.sleep(self.loopDelay)

    def format_data(self, data):
        return data

        # size = str(len(data)).encode()
        # while len(size) != 8:  # 8 bytes to represent the size
        #     size = b"0" + size
        # headers = size
        # return headers + data

    def send_to_all(self, data):
        for client in self.clients:
            self.sock.sendto(self.format_data(data), client)

    def send_to(self, data, client_address):
        self.sock.sendto(self.format_data(data), client_address)
