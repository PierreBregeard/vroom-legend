import pygame
import os
from src.classes.World import World
from src.classes.sprites.Player import Player


class Game:

    def init_player(self):
        imgPath = os.path.abspath("ressources/sprites/player.png")
        img = pygame.image.load(imgPath).convert()
        return Player(0, img, (self.screen_size[0] // 2, self.screen_size[1] // 2))

    def __init__(self):
        self.screen_size = (700, 500)
        self.window = pygame.display.set_mode(self.screen_size)
        self.player = self.init_player()
        self.map = World(self.screen_size)

    def update_player(self):
        keys = pygame.key.get_pressed()
        self.player.handle_keys_press(keys)

    def update(self):
        self.update_player()

    def render(self):
        world_surface = self.map.get_world_surface()
        self.player.blit_car_to_surface(world_surface)

        blit_pos = (self.screen_size[0] / 2 - self.player.x, self.screen_size[1] / 2 - self.player.y)
        self.window.blit(world_surface, blit_pos)

        return

        rotated_window = pygame.transform.rotate(self.window, -self.player.rotation_angle)
        rotated_window_rect = rotated_window.get_rect(center=(self.screen_size[0] / 2, self.screen_size[1] / 2))

        self.window.blit(rotated_window, rotated_window_rect)


        # render = pygame.Surface(world_surface.get_size())
        # # render.fill((255, 255, 255))
        # blit_pos = (self.screen_size[0] / 2 - self.player.x, self.screen_size[1] / 2 - self.player.y)
        #
        # render.blit(world_surface, blit_pos)
        #
        # self.window.blit(render, (0, 0))

        # test = pygame.transform.rotate(self.window, -self.player.rotation_angle)
        # test_rect = test.get_rect(center=(self.screen_size[0] / 2, self.screen_size[1] / 2))
        # self.window.blit(test, test_rect)



        # rotated_render = pygame.transform.rotate(render, -self.player.rotation_angle)
        # blit_pos = (render.get_width() / 2 - rotated_render.get_width() / 2, render.get_height() / 2 - rotated_render.get_height() / 2)
        #
        # self.window.blit(rotated_render, blit_pos)




