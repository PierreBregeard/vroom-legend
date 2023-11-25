import pygame
from pathlib import Path
from .World import World
from .sprites.Player import Player


class Game:

    def init_player(self):
        imgPath = Path("src/ressources/sprites/player.png")
        img = pygame.image.load(imgPath).convert_alpha()
        return Player(0, img, (self.screen_size[0] // 2, self.screen_size[1] // 2))

    def __init__(self):
        self.screen_size = (700, 500)
        self.window = pygame.display.set_mode(self.screen_size)

        self.player = self.init_player()
        self.map = World(self.screen_size)
        self.map.add_sprites(self.player)

    def update_player(self):
        print(self.player.rect.collidelist(self.map.get_collisions_objects()))
        keys = pygame.key.get_pressed()
        self.player.handle_keys_press(keys)
        if self.player.rect.collidelist(self.map.get_collisions_objects()) != -1:
            self.player.velocity = 0
            self.player.undo_move()

    def update(self):
        self.update_player()

    def render(self):
        world_surface = self.map.get_world_surface()
        world_surface = pygame.transform.rotozoom(world_surface, -self.player.angle, 1)
        rect = world_surface.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 2))
        self.window.blit(world_surface, rect)
