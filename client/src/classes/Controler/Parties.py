import requests
from threading import Thread


class ControlerParties:

    @staticmethod
    def save_history(data):

        def f():
            try:
                requests.post("http://127.0.0.1:5000/saveHistory", json=data)
                return
            except requests.exceptions.ConnectionError:
                return

        thread = Thread(target=f)
        thread.start()
