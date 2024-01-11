import json
import socket
from .Socket import Socket
from .ServerProtocol import ServerProtocol
from .ClientProtocol import ClientProtocol
import time


class Server(Socket):
    tick = 0.01
    MAX_CLIENTS = 5

    clients = {}
    is_game_started = False
    start_time = 0

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

    def register_client(self, client_address, infos):
        if client_address not in self.clients:
            if len(self.clients) == self.MAX_CLIENTS:
                self.send_to(ClientProtocol.ERROR.value, "Server is full", client_address)
                return
            # TODO: verifier si le client est dans la db
            self.clients[client_address] = {
                "infos": infos,
                "data": {
                    "pos": (0, 0),
                    "angle": 0,
                    "speed": 0
                }
            }
            print(f"New client connected: {client_address}")
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
        if protocol.value == ServerProtocol.SET_PLAYER_DATA.value:
            # TODO: check if game is started
            # if not self.is_game_started:
            #     self.send_to(ClientProtocol.ERROR.value, "Game is not started", client_address)
            # else:
            # TODO : verif data format (pos, angle, speed)
            self.clients[client_address]["data"] = json.loads(data)
        elif protocol.value == ServerProtocol.REGISTER.value:
            self.register_client(client_address, json.loads(data))
        elif protocol.value == ServerProtocol.START_GAME.value:
            if self.clients[client_address]["infos"]["is_admin"]:
                self.start_time = time.time()
            else:
                self.send_to(ClientProtocol.ERROR.value, "You are not the admin", client_address)
        elif protocol.value == ServerProtocol.DISCONNECT.value:
            if client_address in self.clients:
                self.clients.pop(client_address)
                print(f"Client {client_address} disconnected")
                self.send_to_all(ClientProtocol.PLAYERS_INFOS.value, json.dumps(self.get_players_infos()))
        elif protocol.value == ServerProtocol.PING.value:
            self.send_to(ClientProtocol.PING.value, "", client_address)

    def receive(self):
        try:
            while True:
                yield self.sock.recvfrom(1024)
        except socket.error as e:
            if e.errno in [10035, 11]:
                return
            else:
                raise

    def get_clients_data(self):
        data = {}
        for client in self.clients.values():
            data[client["infos"]["db_id"]] = client["data"]
        return data

    def listen(self):
        start_time = time.time()
        tick_interval = self.tick
        tick_count = 0

        while True:
            tick_count += 1
            targeted_time = start_time + tick_interval * tick_count
            current_time = time.time()
            time_to_wait = targeted_time - current_time
            if time_to_wait > 0:
                time.sleep(time_to_wait)
            else:
                print(f"Server is late by {-time_to_wait}s")

            res = self.receive()
            if not res:
                continue
            for data, client_address in res:
                print(f"Received data from {client_address}: {data}")
                if self.is_game_started and not self.clients[client_address]:
                    self.send_to(ClientProtocol.ERROR.value, "A game is running", client_address)

                self.handle_data(data, client_address)

            if not self.is_game_started and self.start_time != 0:
                time_left = 3 - int(time.time() - self.start_time)
                if time_left == 0:
                    self.is_game_started = True
                    self.send_to_all(ClientProtocol.ACTION.value, "Start game")
                else:
                    self.send_to_all(ClientProtocol.ACTION.value, str(time_left))

            if self.is_game_started:
                self.send_data_to_all(self.get_clients_data())

    def send_to_all(self, protocol: str, data: str):
        for client_address in self.clients:
            self.send_to(protocol, str(data), client_address)

    def send_data_to_all(self, data):
        for client_address in self.clients:
            data_to_send = data.copy()
            data_to_send.pop(self.clients[client_address]["infos"]["db_id"])
            self.send_to(ClientProtocol.DATA.value, json.dumps(data_to_send), client_address)

    def send_to(self, protocol: str, data: str, client_address):
        self.sock.sendto((protocol + data).encode(), client_address)
