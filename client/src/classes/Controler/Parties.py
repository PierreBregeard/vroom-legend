import json

import requests
from threading import Thread
from .API import API


class ControlerParties:

    @staticmethod
    def save_history(data):

        def f():
            try:
                requests.post(API.URL + "saveHistory", json=data)
                return
            except requests.exceptions.ConnectionError:
                return

        thread = Thread(target=f)
        thread.start()

    @staticmethod
    def get_parties(pseudo):
        try:
            response = requests.post(API.URL + "getHistory", json=pseudo)
            parties = response.content.decode()
            return json.loads(parties)
        except requests.exceptions.ConnectionError:
            return
