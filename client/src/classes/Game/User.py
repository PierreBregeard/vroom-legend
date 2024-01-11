import pygame
from ..ResourcePath import RelativePath
from ..Controler.Log import Log


class User:
    pseudo = ""


    @staticmethod
    def connexion(logs):
        res = Log.connexion(logs)
        if res is not None:
            User.pseudo = res.decode()
            return True
        else:
            return False
