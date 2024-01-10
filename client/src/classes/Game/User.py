import pygame
from ..ResourcePath import RelativePath
from ..Controler.Log import connexion


class User:

    pseudo = ""

    @staticmethod
    def connexion(log):
        User.pseudo = connexion(log)