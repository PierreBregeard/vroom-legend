import pygame
from pathlib import Path
from os import chdir
from classes.Game import Game
from classes.Multiplayer import Multiplayer

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

    clock.tick(60)
    game.update()
    game.render()
    pygame.display.flip()

multi.close_multiplayer()
pygame.quit()
