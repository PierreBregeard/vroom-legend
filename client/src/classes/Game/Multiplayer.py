from ..UDP.Server import Server
from ..UDP.Client import Client
import uuid


class Multiplayer:

    def start_server(self):
        serv = Server(self.addr, self.port)
        print(f"Server started on {self.addr}:{self.port}")
        serv.listen()

    def register_server(self):
        # map ip with rdm string in the db
        pass

    def connect_to_server(self):
        # get ip from db
        # todo: ping le serveur pour savoir si il est toujours actif
        # todo: récupérer l'ip du serveur depuis la db ansi que la bd_id du client
        return Client(self.addr, self.port, str(uuid.uuid4()))

    def close_multiplayer(self):
        self.client.diconnect()
        # todo: delete ip from db

    def __init__(self, is_server: bool, addr=None, port=5000):
        if is_server:
            from threading import Thread
            self.addr = Server.get_ipv4_address()
            self.port = 5000
            self.thread = Thread(target=self.start_server, daemon=True)
            # deamon = True -> stop thread when main thread is stopped
            self.thread.start()
            self.register_server()
        else:
            if addr is None:
                raise ValueError("addr must be specified when is_server is False")
            self.addr = addr  # todo: get ip from db
            self.port = port

        self.client = self.connect_to_server()
        self.client.register()
