import pygame
from pathlib import Path
from os import chdir

from src.classes.Game.Game import Game
from src.classes.Menu.menu import Menu

game_size = (1500, 900)

chdir(Path(__file__).parent)

pygame.init()
game = Game(enable_screen_rotation=False, width=game_size[0], height=game_size[1])

menu = Menu(width=game_size[0], height=game_size[1])
menu.menu(game)
