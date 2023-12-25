import pygame
import pyscroll
import pytmx
from math import sqrt, ceil


class World:

    def __init__(self, map_path, screen_size, enable_screen_rotation):
        tmx_data = pytmx.util_pygame.load_pygame(map_path)

        map_data = pyscroll.data.TiledMapData(tmx_data)
        if enable_screen_rotation:
            square_size = ceil(sqrt(screen_size[0] ** 2 + screen_size[1] ** 2))
            self.map_size = (square_size, square_size)
        else:
            self.map_size = screen_size

        self.map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.map_size)
        self.group = pyscroll.PyscrollGroup(self.map_layer, default_layer=1)

        # List des objets avec collision
        self.walls = []
        for obj in tmx_data.objects:
            if obj.type == "Collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        # List des checkpoints
        self.checkpoints = []
        for obj in tmx_data.objects:
            if obj.type == "checkpoint":
                self.checkpoints.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    def set_soom(self, zoom):
        self.map_layer.zoom = zoom

    def add_sprites(self, sprites):
        self.group.add(sprites)

    def get_world_surface(self):
        surface = pygame.Surface(self.map_size)
        self.group.center(self.group.get_sprite(0).rect.center)
        self.group.draw(surface)
        return surface

    def get_collisions_objects(self):
        return self.walls

    def get_checkpoints(self) -> object:
        return self.checkpoints
