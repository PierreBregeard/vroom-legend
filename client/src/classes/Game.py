import pygame
from pathlib import Path
from .World import World
from .sprites.Player import Player


class Game:

    def init_player(self):
        imgPath = Path("src/ressources/sprites/player.png")
        img = pygame.image.load(imgPath).convert_alpha()
        return Player(0, img, (500, 500))

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
        if self.player.rect.collidelist(self.map.get_collisions_objects()) != -1:
            self.player.velocity = 0
            self.player.undo_move()

    def update(self):
        self.update_player()

    def update_hud(self):
        needle = pygame.image.load("src//ressources//sprites//needle.png").convert_alpha()
        speedometer = pygame.image.load("src//ressources//sprites//speedometer.png").convert_alpha()
        speedometer_rect = speedometer.get_rect()
        speedometer_rect.center = (self.screen_size[0] - 100, self.screen_size[1] - 100)

        angle = 140
        angle -= abs(self.player.velocity) * 20

        needle_rotated = pygame.transform.rotate(needle, angle)
        needle_rect = needle_rotated.get_rect(center=speedometer_rect.center)

        self.window.blit(speedometer, speedometer_rect)
        self.window.blit(needle_rotated, needle_rect)

    def render(self):
        world_surface = self.map.get_world_surface()
        if self.enable_screen_rotation:
            world_surface = pygame.transform.rotozoom(world_surface, -self.player.angle, 1)
        rect = world_surface.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 2))
        self.window.blit(world_surface, rect)
