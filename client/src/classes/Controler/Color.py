import json

import requests
from ..Game.User import User

from src.classes.Game.User import User


class ControllerColor:

    @staticmethod
    def get_color():
        data = {"pseudo": User.pseudo}
        try:
            response = requests.post("http://127.0.0.1:5000/couleur", json=data)
            json_str = response.text.replace("'", '"')
            color = json.loads(json_str)
            return color
        except requests.exceptions.ConnectionError:
            return None


    @staticmethod
    def change_color(data):
        try:
            response = requests.post("http://127.0.0.1:5000/changeCoul", json=data)
            print(response.status_code)
            print(response.content)
            return response.content
        except requests.exceptions.ConnectionError:
            return None