from .Socket import Socket
from .ServerProtocol import ServerProtocol
from .ClientProtocol import ClientProtocol
import json
import socket


class Client(Socket):
    tick = 0.01
    last_send_time = 0

    def __init__(self, ip, port, db_id):
        super().__init__()
        self.db_id = db_id
        self.sock.connect((ip, port))

    def send_player_data(self, player_data):
        # todo : implement tick rate ?
        data = json.dumps(player_data)
        self.send(ServerProtocol.SET_PLAYER_DATA.value, data)

    def register(self):
        self.send(ServerProtocol.REGISTER.value, self.db_id)
        # protocol, data = self.receive()
        # if protocol == ClientProtocol.SUCCESS:
        #     print("Registered successfully")
        # else:
        #     raise Exception(data)

    def diconnect(self):
        pass
        # self.send(ServerProtocol.DISCONNECT.value, self.db_id)  # todo: disconnect protocol

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

    def send(self, protocol: str, data: str):
        self.sock.send((protocol + data).encode())
