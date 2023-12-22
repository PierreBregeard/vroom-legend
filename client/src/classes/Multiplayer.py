from .UDP.Server import Server


class Multiplayer:

    def start_server(self):
        serv = Server(self.addr, self.port)
        serv.listen()

    def register_server(self):
        pass



    def __init__(self, is_server: bool):
        if is_server:
            from threading import Thread
            self.addr = Server.get_ipv4_address()
            self.port = 5000
            Thread(target=self.start_server).start()
            self.register_server()
        else
