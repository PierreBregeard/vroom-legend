import socket
from .Socket import Socket
from .ServerProtocol import ServerProtocol
import time


class Server(Socket):
    tick = 10 / 1000  # tick rate for server response
    loopDelay = 0.1  # prevent big CPU usage
    MAX_CLIENTS = 2

    clients = {}
    is_game_started = False
    clients_data = {}

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

    def register_client(self, client_address, db_id):
        if client_address not in self.clients:
            if len(self.clients) == self.MAX_CLIENTS:
                self.send_to("Server is full", client_address)
                return
            # TODO: verifier si le client est dans la db
            self.clients[client_address] = {
                "db_id": db_id,
                "is_admin": len(self.clients) == 0  # first client is admin
            }
            print(f"New client connected: {client_address}")
            self.send_to("ok", client_address)
        else:
            self.send_to("You are already connected", client_address)

    def handle_data(self, data, client_address):
        raw_protocol = data.decode()[0]
        data = data.decode()[1:]
        if not ServerProtocol.is_valid(raw_protocol):
            self.send_to("Invalid protocol", client_address)
            return

        protocol = ServerProtocol(raw_protocol)
        if protocol == ServerProtocol.SET_PLAYER_DATA:
            if not self.is_game_started:
                self.send_to("Game is not started", client_address)
            else:
                # TODO : verif data format (pos, angle, speed)
                db_id = self.clients[client_address].db_id
                self.clients_data[db_id] = data
        elif protocol == ServerProtocol.REGISTER:
            self.register_client(client_address, data)
        elif protocol == ServerProtocol.GET_PLAYERS_IDs:
            self.send_to(str([client.db_id for client in self.clients]), client_address)
        elif protocol == ServerProtocol.START_GAME:
            if self.clients[client_address].is_admin:
                self.is_game_started = True
                self.send_to_all("Start game")
            else:
                self.send_to("You are not the admin", client_address)

    def receive(self):
        try:
            data, client_address = self.sock.recvfrom(1024)

            if self.is_game_started and not self.clients[client_address]:
                self.send_to("A game is running", client_address)
                return True

            self.handle_data(data, client_address)
            return True

        except socket.error as e:
            if e.errno in [10035, 11]:
                return False
            else:
                raise

    def listen(self):
        next_tick_time = time.time() + self.tick
        while True:
            while self.receive():
                pass

            self.send_to_all(str(self.clients_data))
            self.clients_data = {}

            current_time = time.time()
            if current_time >= next_tick_time:
                next_tick_time = current_time + self.tick
            time.sleep(self.loopDelay)

    def send_to_all(self, data: str):
        for client_address in self.clients:
            self.send_to(str(data), client_address)

    def send_to(self, data: str, client_address):
        self.sock.sendto(data.encode(), client_address)
