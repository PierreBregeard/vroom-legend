import pygame

from src.game import Game
from src.player import Player
from src.world import World

pygame.init()
clock = pygame.time.Clock()
game = Game()

run = True

while run:
    # Verify if game is closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    clock.tick(60)
    game.update()
    pygame.display.flip()

pygame.quit()
