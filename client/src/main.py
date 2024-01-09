import pygame
from pathlib import Path
from os import chdir
from classes.Game import Game
from classes.Multiplayer import Multiplayer
from classes.ColorCar import ColorCar

from src.classes.Game.Game import Game
from src.classes.Menu.menu import Menu

game_size = (1500, 900)

chdir(Path(__file__).parent)

multi = Multiplayer(is_server=True)
game = Game(multi)
clock = pygame.time.Clock()
pygame.init()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
pygame.init()
game = Game(enable_screen_rotation=False, width=game_size[0], height=game_size[1])

menu = Menu(width=game_size[0], height=game_size[1])
menu.menu(game)
    clock.tick(60)
    game.update()
    game.render()
    pygame.display.flip()

multi.close_multiplayer()
ColorCar.remove_temp_files()
pygame.quit()
