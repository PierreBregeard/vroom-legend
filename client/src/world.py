import pygame
from pygame import transform
import pyscroll
import pytmx


class World():

    def __init__(self, screen_size):
        tmx_data = pytmx.util_pygame.load_pygame("src/ressources/Maps/FirstMap.tmx")

        map_data = pyscroll.data.TiledMapData(tmx_data)

        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, screen_size)
        map_layer.zoom = 1.8


        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)

    def drawWorld(self, window, center):
        self.group.center(center)
        self.group.draw(window)

