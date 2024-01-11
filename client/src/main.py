import pygame
from pathlib import Path
from os import chdir

from classes.Menu.Menu import Menu

chdir(Path(__file__).parent)


# def get_screen_size():
#     pygame.init()
#     screen_info = pygame.display.Info()
#     screen_width = screen_info.current_w
#     screen_height = screen_info.current_h
#     pygame.quit()
#     return screen_width, screen_height
#
#
# game_height = get_screen_size()[1] - 100
# game_size = game_height, game_height

pygame.init()
native_resolution = (750, 750)
info = pygame.display.Info()
current_resolution = (info.current_w, info.current_h)
scale_factor = min(current_resolution[0] / native_resolution[0], current_resolution[1] / native_resolution[1])
window = pygame.display.set_mode(native_resolution, pygame.SCALED)

menu = Menu(game_size=native_resolution)
menu.menu()
