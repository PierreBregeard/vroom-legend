import requests
from .API import API


class Log:

    @staticmethod
    def connexion(data):
        response = requests.post(API.URL + "connexion", json=data)
        print(response.content)
        return response.content
