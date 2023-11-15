import pygame
import pyscroll
import pytmx
from pathlib import Path


class World:

    def __init__(self, screen_size):
        map_path = Path("src/ressources/Maps/FirstMap.tmx")
        tmx_data = pytmx.util_pygame.load_pygame(map_path)

        map_data = pyscroll.data.TiledMapData(tmx_data)
        self.map_size = map_data.map_size[0] * map_data.tile_size[0], map_data.map_size[1] * map_data.tile_size[1]
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.map_size)

        self.group = pyscroll.PyscrollGroup(map_layer, default_layer=1)

    def get_world_surface(self):
        surface = pygame.Surface(self.map_size)
        self.group.draw(surface)
        return surface
