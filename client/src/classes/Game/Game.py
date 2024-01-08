import time

import pygame
from src.classes.ResourcePath import RelativePath
from src.classes.Game.World import World
from src.classes.sprites.Player import Player
from src.classes.sprites.ColorCar import ColorCar
from src.classes.HUD.HUD import HUD


class Game:

    def init_player(self):
        color_car = ColorCar()
        color_car.set_roof_color((0, 100, 0))
        color_car.set_base_color((100, 0, 100))
        imgPath = color_car.save_img()
        img = pygame.image.load(imgPath).convert_alpha()
        return Player(0, img, (500, 500))

    def __init__(self, enable_screen_rotation=True, width=600, height=600):
        self.screen_size = (width, height)
        self.enable_screen_rotation = enable_screen_rotation
        self.window = pygame.display.set_mode(self.screen_size)

        self.start_time = time.time()
        self.player = self.init_player()
        self.HUD = HUD(self.screen_size, self.player.max_speed)

        map_path = RelativePath.resource_path("ressources\\Maps\\dependencies\\FirstMap.tmx")
        self.map = World(map_path, self.screen_size, self.enable_screen_rotation)
        self.map.set_soom(1)
        self.map.add_sprites(self.player)
        # List of boolean for already visited checkpoints
        self.has_missed_checkpoint = False
        self.checkpoints_list = []
        for i in range(0, len(self.map.get_checkpoints())):
            self.checkpoints_list.append(False)

    def play(self):
        clock = pygame.time.Clock()
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            clock.tick(60)
            self.update()
            self.render()
            pygame.display.flip()

    def update_player(self):
        keys = pygame.key.get_pressed()
        self.player.handle_keys_press(keys)

        objects = self.map.get_collisions_objects()
        if self.player.rect.collidelist(self.map.get_collisions_objects()) != -1:
            self.player.velocity = 0
            self.player.undo_move()
            # Trying to make the player move on x axis if collision only on y, and move y axis if only on x
            for object in objects:
                if self.player.rect.x < object.x + object.width and self.player.rect.x + self.player.rect.width > object.x:
                    self.player.undo_move_x()
                if self.player.rect.y < object.y + object.height and self.player.rect.y + self.player.rect.height > object.y:
                    self.player.undo_move_y()

    def verify_checkpoints(self):
        # Index of the checkpoint player is on
        idx = self.player.rect.collidelistall(self.map.get_checkpoints())

        # Index of the checkpoint player passed
        idx_passed = self.player.rect.collidelistall(self.map.get_missed_checkpoints())

        # If there is and indice,
        # If it is not already visited
        # If last checkpoint is visited, or it is the first checkpoint
        if len(idx) and not self.checkpoints_list[idx[0]] and (self.checkpoints_list[idx[0] - 1] or idx[0] == 0):
            # Player visited a new checkpoint
            self.checkpoints_list[idx[0]] = True
            print("Player passed a checkpoint !")
            self.HUD.has_missed_checkpoint = False
        try:
            idx_last_visited_checkpoint = next(x for x, val in enumerate(self.checkpoints_list) if val == False)-1
            if (not (idx_last_visited_checkpoint == -1) and
                    len(idx_passed) and
                    idx_passed[0] > idx_last_visited_checkpoint and
                    idx_passed[0] == idx_last_visited_checkpoint+1):
                self.HUD.has_missed_checkpoint = True
        except:
            print("Player have passed all checkpoints")



    def update(self):
        self.update_player()
        self.verify_checkpoints()
        self.HUD.speedometer.speed = self.player.velocity

    def render(self):
        world_surface = self.map.get_world_surface()
        if self.enable_screen_rotation:
            world_surface = pygame.transform.rotozoom(world_surface, -self.player.angle, 1)
        rect = world_surface.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 2))
        self.window.blit(world_surface, rect)
        self.HUD.blit_HUD(self.window, self.checkpoints_list, time.time() - self.start_time)
