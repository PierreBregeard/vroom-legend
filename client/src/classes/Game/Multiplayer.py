from ..UDP.Server import Server
from ..UDP.Client import Client
import uuid
import socket


class Multiplayer:

    def start_server(self):
        self.serv = Server(self.addr, self.port)
        print(f"Server started on {self.addr}:{self.port}")
        self.serv.listen()

    def connect_to_server(self):
        try:
            return Client(self.addr, self.port, str(uuid.uuid4()))
        except socket.gaierror:
            return None

    def close_multiplayer(self):
        self.client.diconnect()
        if self.client.is_admin:
            self.serv.is_server_running = False

    def __init__(self, is_server: bool, addr=None, port=5000):
        self.serv = None
        if is_server:
            from threading import Thread
            self.addr = Server.get_ipv4_address()
            self.port = 5000
            self.thread = Thread(target=self.start_server, daemon=True)
            # deamon = True -> stop thread when main thread is stopped
            self.thread.start()
        else:
            if addr is None:
                raise ValueError("addr must be specified when is_server is False")
            self.addr = addr
            self.port = port

        self.client = self.connect_to_server()
        if self.client:
            self.client.is_admin = is_server
