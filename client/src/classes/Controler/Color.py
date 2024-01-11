import json

import requests


class ControllerColor:

    @staticmethod
    def get_color(data):
        try:
            response = requests.post("http://127.0.0.1:5000/couleur", json=data)
            if response.content:
                json_str = response.text.replace("'", '"')
                return json.loads(json_str)
        except requests.exceptions.ConnectionError:
            return None

    @staticmethod
    def change_color(data):
        try:
            response = requests.post("http://127.0.0.1:5000/changeCoul", json=data)
            return response.content
        except requests.exceptions.ConnectionError:
            return
