from ..Controler.Color import ControllerColor
from ..Controler.Log import ControlerLog


class User:
    pseudo = ""
    color1 = (100, 0, 0)
    color2 = (0, 100, 0)

    @staticmethod
    def connexion(logs):
        res = ControlerLog.connexion(logs)
        if res:
            User.pseudo = res.decode()
            User.fetch_color()

    @staticmethod
    def fetch_color():
        colors = ControllerColor.get_color({"pseudo": User.pseudo})
        if colors:
            User.color1, User.color2 = colors["color1"], colors["color2"]
