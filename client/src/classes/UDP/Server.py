import json
import socket
from .Socket import Socket
from .ServerProtocol import ServerProtocol
from .ClientProtocol import ClientProtocol
import time


class Server(Socket):
    tick = 10 / 1000  # tick rate for server response
    loopDelay = 0.1  # prevent big CPU usage
    MAX_CLIENTS = 2

    clients = {}
    is_game_started = False

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

    def register_client(self, client_address, db_id):
        if client_address not in self.clients:
            if len(self.clients) == self.MAX_CLIENTS:
                self.send_to(ClientProtocol.ERROR.value, "Server is full", client_address)
                return
            # TODO: verifier si le client est dans la db
            self.clients[client_address] = {
                "infos": {
                    "db_id": db_id,
                    "name": "test",
                },
                "data": {
                    "pos": (0, 0),
                    "angle": 0,
                    "speed": 0
                },
                "is_admin": len(self.clients) == 0  # first client is admin
            }
            print(f"New client connected: {client_address}")
            self.send_to(ClientProtocol.SUCCESS.value, "", client_address)
            self.send_to_all(ClientProtocol.PLAYERS_INFOS.value, json.dumps(self.get_players_infos()))
        else:
            self.send_to(ClientProtocol.ERROR.value, "You are already connected", client_address)

    def get_players_infos(self):
        # TODO: get players infos from db colors, names, etc...
        return [self.clients[client]["infos"] for client in self.clients]

    def handle_data(self, data, client_address):
        raw_protocol = data.decode()[0]
        data = data.decode()[1:]
        if not ServerProtocol.is_valid(raw_protocol):
            self.send_to(ClientProtocol.ERROR.value, "Invalid protocol", client_address)
            return

        protocol = ServerProtocol(raw_protocol)
        if protocol == ServerProtocol.SET_PLAYER_DATA:
            # TODO: check if game is started
            # if not self.is_game_started:
            #     self.send_to(ClientProtocol.ERROR.value, "Game is not started", client_address)
            # else:
            # TODO : verif data format (pos, angle, speed)
            self.clients[client_address]["data"] = json.loads(data)
        elif protocol == ServerProtocol.REGISTER:
            self.register_client(client_address, data)
        elif protocol == ServerProtocol.START_GAME:
            if self.clients[client_address].is_admin:
                self.is_game_started = True
                self.send_to_all(ClientProtocol.ACTION.value, "Start game")
            else:
                self.send_to(ClientProtocol.ERROR.value, "You are not the admin", client_address)

    def receive(self):
        try:
            data, client_address = self.sock.recvfrom(1024)

            if self.is_game_started and not self.clients[client_address]:
                self.send_to(ClientProtocol.ERROR.value, "A game is running", client_address)
                return True

            self.handle_data(data, client_address)
            return True

        except socket.error as e:
            if e.errno in [10035, 11]:
                return False
            else:
                raise

    def get_clients_data(self):
        data = {}
        for client in self.clients.values():
            data[client["infos"]["db_id"]] = client["data"]
        return json.dumps(data)


    def listen(self):
        next_tick_time = time.time() + self.tick
        while True:
            while self.receive():
                pass

            self.send_to_all(ClientProtocol.DATA.value, self.get_clients_data())

            current_time = time.time()
            if current_time >= next_tick_time:
                next_tick_time = current_time + self.tick
            time.sleep(self.loopDelay)

    def send_to_all(self, protocol: str, data: str):
        for client_address in self.clients:
            self.send_to(protocol, str(data), client_address)

    def send_to(self, protocol: str, data: str, client_address):
        self.sock.sendto((protocol + data).encode(), client_address)
