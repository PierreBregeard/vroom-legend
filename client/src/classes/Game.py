import pygame
import os
import sys
from pathlib import Path
from .World import World
from .sprites.Player import Player


class Game:
    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def init_player(self):
        imgPath = self.resource_path("src\\ressources\\sprites\\player.png")
        img = pygame.image.load(imgPath).convert_alpha()
        return Player(0, img, (500, 500))

    def __init__(self, enable_screen_rotation=True):
        self.screen_size = (600, 600)
        self.enable_screen_rotation = enable_screen_rotation
        self.window = pygame.display.set_mode(self.screen_size)

        self.player = self.init_player()
        map_path = self.resource_path("src\\ressources\\Maps\\FirstMap.tmx")
        self.map = World(map_path, self.screen_size, self.enable_screen_rotation)
        self.map.set_soom(1)
        self.map.add_sprites(self.player)

    def update_player(self):
        keys = pygame.key.get_pressed()
        self.player.handle_keys_press(keys)
        if self.player.rect.collidelist(self.map.get_collisions_objects()) != -1:
            self.player.velocity = 0
            self.player.undo_move()

    def update(self):
        self.update_player()

    def render(self):
        world_surface = self.map.get_world_surface()
        if self.enable_screen_rotation:
            world_surface = pygame.transform.rotozoom(world_surface, -self.player.angle, 1)
        rect = world_surface.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 2))
        self.window.blit(world_surface, rect)
