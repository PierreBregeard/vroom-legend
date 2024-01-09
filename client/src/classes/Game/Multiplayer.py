from src.classes.UDP.Server import Server
from src.classes.UDP.Client import Client
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

        # todo: récupérer l'ip du serveur depuis la db ansi que la bd_id du client
        return Client(self.addr, self.port, str(uuid.uuid4()))

    def close_multiplayer(self):
        self.client.diconnect()
        # todo: delete ip from db

    def __init__(self, is_server: bool):
        # tmp
        self.addr = Server.get_ipv4_address()
        self.port = 5000

        if is_server:
            from threading import Thread
            # self.addr = Server.get_ipv4_address()
            # self.port = 5000
            self.thread = Thread(target=self.start_server, daemon=True)
            # deamon = True -> stop thread when main thread is stopped
            self.thread.start()
            self.register_server()

        self.client = self.connect_to_server()
        self.client.register()
