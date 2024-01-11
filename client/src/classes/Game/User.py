import pygame
from ..ResourcePath import RelativePath
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
            return True
        else:
            return False
