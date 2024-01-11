import json

import requests


class Color:

    @staticmethod
    def get_color(data):
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
            return True
        except requests.exceptions.ConnectionError:
            return None