import pygame
from pathlib import Path
from os import chdir

from classes.Game.Game import Game
from classes.Menu.Menu import Menu

game_size = (1500, 900)

chdir(Path(__file__).parent)

pygame.init()
game = Game(enable_screen_rotation=False, game_size=game_size)

menu = Menu(game_size=game_size)
menu.menu(game)
