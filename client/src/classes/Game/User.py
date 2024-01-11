import pygame
from ..ResourcePath import RelativePath
from ..Controler.Log import ControlerLog


class User:
    pseudo = ""
    color1 = tuple
    color2 = tuple


    @staticmethod
    def connexion(logs):
        res = ControlerLog.connexion(logs)
        if res is not None:
            User.pseudo = res.decode()
            return True
        else:
            return False
