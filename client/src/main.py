import pygame
from pathlib import Path
from os import chdir

from classes.Game import Game

chdir(Path(__file__).parent)

IS_SERVER = True
if IS_SERVER:

    from classes.UDP.Client import Client
    client = Client(addr, port)
    client.send(b"Hellow world!")
    data = client.receive()
    print(data)



# pygame.init()
# clock = pygame.time.Clock()
# game = Game(enable_screen_rotation=False)
#
# run = True
# while run:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False
#
#     clock.tick(60)
#     game.update()
#     game.render()
#     pygame.display.flip()
#
# pygame.quit()
