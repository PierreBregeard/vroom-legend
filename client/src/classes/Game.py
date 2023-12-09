import pygame
from pathlib import Path
from .World import World
from .sprites.Player import Player


class Game:

    def init_player(self):
        imgPath = Path("src/ressources/sprites/player.png")
        img = pygame.image.load(imgPath).convert_alpha()
        return Player(0, img, (self.screen_size[0] // 2, self.screen_size[1] // 2))

    def __init__(self, enable_screen_rotation=True):
        self.screen_size = (600, 600)
        self.enable_screen_rotation = enable_screen_rotation
        self.window = pygame.display.set_mode(self.screen_size)

        self.player = self.init_player()
        self.map = World(self.screen_size, self.enable_screen_rotation)
        self.map.set_soom(1)
        self.map.add_sprites(self.player)

    def update_player(self):
        keys = pygame.key.get_pressed()
        self.player.handle_keys_press(keys)

    def update(self):
        self.update_player()

    def render(self):
        world_surface = self.map.get_world_surface()
        if self.enable_screen_rotation:
            world_surface = pygame.transform.rotozoom(world_surface, -self.player.angle, 1)
        rect = world_surface.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 2))
        self.window.blit(world_surface, rect)




