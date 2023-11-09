import pygame

from src.player import Player
from src.world import World


class Game:

    def __init__(self):
        # screen_size = (width, height)
        self.screen_size = (700, 500)
        self.window = pygame.display.set_mode(self.screen_size)
        self.player = Player(self.window)
        self.map = World(self.screen_size)

    def update(self):
        # Get all pressed keys

        keys = pygame.key.get_pressed()

        self.map.drawWorld(self.window, self.player.getCenter())
        self.player.drawPlayer(keys)


