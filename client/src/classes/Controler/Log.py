import requests
from .API import API


class ControlerLog:

    @staticmethod
    def connexion(data):
        try:
            response = requests.post(API.URL + "connexion", json=data)
            print(response.content)
            return response.content
        except requests.exceptions.ConnectionError:
            return None

    @staticmethod
    def inscription(data):
        try:
            response = requests.post(API.URL + "inscription", json=data)
            return True
        except requests.exceptions.ConnectionError:
            return None
