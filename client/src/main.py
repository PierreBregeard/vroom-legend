import pygame
from pathlib import Path
from os import chdir

from classes.Menu.Menu import Menu

chdir(Path(__file__).parent)


def get_screen_size():
    pygame.init()
    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h
    pygame.quit()
    return screen_width, screen_height


game_height = get_screen_size()[1] - 100
game_size = game_height, game_height

pygame.init()
menu = Menu(game_size=game_size)
menu.menu()
