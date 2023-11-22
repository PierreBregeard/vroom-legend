import pygame
import pyscroll
import pytmx
from pathlib import Path


class World:

    def __init__(self, screen_size):
        map_path = str(Path("src/ressources/Maps/FirstMap.tmx"))
        tmx_data = pytmx.util_pygame.load_pygame(map_path)

        map_data = pyscroll.data.TiledMapData(tmx_data)
        # self.map_size = screen_size
        self.map_size = (1000, 1000)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.map_size)
        self.group = pyscroll.PyscrollGroup(self.map_layer, default_layer=1)

    def set_soom(self, zoom):
        self.map_layer.zoom = zoom

    def add_sprites(self, sprites):
        self.group.add(sprites)

    def get_world_surface(self):
        surface = pygame.Surface(self.map_size)
        self.group.center(self.group.get_sprite(0).rect.center)
        self.group.draw(surface)
        return surface
