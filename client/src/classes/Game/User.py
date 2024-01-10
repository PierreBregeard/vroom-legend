import pygame
from ..ResourcePath import RelativePath
from ..Controler.Log import Log


class User:
    pseudo = ""


    @staticmethod
    def connexion(logs):
        res = Log.connexion(logs)
        User.pseudo = res.decode()
