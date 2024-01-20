import json

import requests

from .API import API


class ControllerColor:

    @staticmethod
    def get_color(data):
        try:
            response = requests.post(API.URL + "couleur", json=data)
            if response.content:
                json_str = response.text.replace("'", '"')
                return json.loads(json_str)
        except requests.exceptions.ConnectionError:
            return None

    @staticmethod
    def change_color(data):
        try:
            response = requests.post(API.URL + "changeCoul", json=data)
            return
        except requests.exceptions.ConnectionError:
            return
