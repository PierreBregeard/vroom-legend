from .Socket import Socket
from .ServerProtocol import ServerProtocol
import json


class Client(Socket):

    def __init__(self, ip, port):
        super().__init__()
        self.sock.connect((ip, port))

    def send_player_data(self, player_data):
        # todo : implement tick rate ?
        data = ServerProtocol.SET_PLAYER_DATA.value
        data += json.dumps(player_data)
        self.send(data)

    def receive(self):
        data = self.sock.recvfrom(1024)
        return data

    def send(self, data: str):
        self.sock.send(data.encode())
