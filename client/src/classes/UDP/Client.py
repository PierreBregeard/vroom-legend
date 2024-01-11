from .Socket import Socket
from .ServerProtocol import ServerProtocol
from .ClientProtocol import ClientProtocol
import json
import socket
import time


class Client(Socket):

    is_admin = False

    def ping(self):
        self.send(ServerProtocol.PING.value, "")

        start = time.time()
        while time.time() - start < 2:
            raw_data = list(self.receive())
            if not raw_data:
                continue
            for raw_protocol, data in raw_data:
                if raw_protocol == ClientProtocol.PING:
                    return True
        return False

    def __init__(self, ip, port, db_id):
        super().__init__()
        self.db_id = db_id
        self.sock.connect((ip, port))
        if not self.ping():
            raise socket.gaierror("Server not found")

    def send_player_data(self, player_data):
        data = json.dumps(player_data)
        self.send(ServerProtocol.SET_PLAYER_DATA.value, data)

    def register(self, pseudo, colorCar):
        # todo: fetch data from db here or in the multi class
        registration_data = json.dumps({
            "db_id": self.db_id,
            "pseudo": pseudo,
            "colors": {
                "base": colorCar.base_color,
                "roof": colorCar.roof_color
            },
            "is_admin": self.is_admin
        })
        self.send(ServerProtocol.REGISTER.value, registration_data)

    def diconnect(self):
        self.send(ServerProtocol.DISCONNECT.value, self.db_id)

    def receive(self):
        try:
            while True:
                data = self.sock.recvfrom(1024)[0]
                raw_protocol = data.decode()[0]
                data = data.decode()[1:]
                if not ClientProtocol.is_valid(raw_protocol):
                    raise Exception("Invalid protocol")

                protocol = ClientProtocol(raw_protocol)
                yield protocol, data
        except socket.error as e:
            if e.errno in [10035, 11]:
                return
            else:
                raise

    def start_game(self):
        self.send(ServerProtocol.START_GAME.value, "")

    def send(self, protocol: str, data: str):
        self.sock.send((protocol + data).encode())
