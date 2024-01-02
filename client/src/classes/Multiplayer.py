from .UDP.Server import Server
from .UDP.Client import Client
from .UDP.ClientProtocol import ClientProtocol


class Multiplayer:

    def start_server(self):
        serv = Server(self.addr, self.port)
        serv.listen()

    def register_server(self):
        # map ip with rdm string in the db
        pass

    def connect_to_server(self):
        # get ip from db

        # tmp
        return Client(self.addr, self.port)

    def __init__(self, is_server: bool):
        # tmp
        self.addr = Server.get_ipv4_address()
        self.port = 5000

        if is_server:
            from threading import Thread
            # self.addr = Server.get_ipv4_address()
            # self.port = 5000
            Thread(target=self.start_server).start()
            self.register_server()

        self.client = self.connect_to_server()
        self.client.register("db_id_test")  # todo: get db id from db
