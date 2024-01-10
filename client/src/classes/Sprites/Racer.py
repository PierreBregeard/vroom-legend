from .Car import Car
import pygame


class Racer(Car):

    def __init__(self, idx, pseudo, img, start_pos):
        super().__init__(idx, img, start_pos)
        self.pseudo = pseudo
