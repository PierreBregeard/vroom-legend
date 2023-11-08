import pygame
import pyscroll
import pytmx

from src.data.player import Player
from src.world import World

pygame.init()

screenHeight = 500
screenWidth = 700
screenSize = (screenWidth, screenWidth)

window = pygame.display.set_mode(screenSize)
clock = pygame.time.Clock()
    
player = Player(window)
map = World(screenSize)

vel = 5

run = True
while run:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # if event.type == pygame.KEYDOWN:
        #     print(pygame.key.name(event.key))

    keys = pygame.key.get_pressed()


    map.drawWorld(window, player.getCenter())
    player.drawPlayer(keys)
    pygame.display.flip()

pygame.quit()
