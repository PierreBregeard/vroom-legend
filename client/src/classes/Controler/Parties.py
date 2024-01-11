import requests


class ControlerParties:

    @staticmethod
    def save_history(data):
        try:
            response = requests.post("http://127.0.0.1:5000/saveHistory", json=data)
            print(response.content)
            return response.content
        except requests.exceptions.ConnectionError:
            return None
