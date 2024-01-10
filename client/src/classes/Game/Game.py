import time

import pygame
from ..ResourcePath import RelativePath
from .World import World
from ..Sprites.Player import Player
from ..Sprites.Racer import Racer
from ..Sprites.ColorCar import ColorCar
from ..HUD.HUD import HUD
from ..UDP.ClientProtocol import ClientProtocol
from ..Sprites.GameTag import GameTag
import json


class Game:
    is_game_started = False

    def init_player(self):
        color_car = ColorCar()
        color_car.set_roof_color((100, 0, 0))
        color_car.set_base_color((0, 100, 100))
        if self.multi:
            self.multi.client.register("Moi", color_car)
        imgPath = color_car.save_img()
        img = pygame.image.load(imgPath).convert_alpha()
        return Player(0, img, (500, 500))

    def __init__(self, enable_screen_rotation, game_size, multi=None):
        self.multi = multi
        self.enable_screen_rotation = enable_screen_rotation
        self.racers = {}
        self.screen_size = game_size
        self.window = pygame.display.set_mode(self.screen_size)

        self.start_time = time.time()
        self.player = self.init_player()
        self.HUD = HUD(self.screen_size, self.player.max_speed)

        map_path = RelativePath.resource_path("ressources/Maps/dependencies/FirstMap.tmx")
        self.map = World(map_path, self.screen_size, self.enable_screen_rotation)
        self.map.set_soom(1)
        self.map.add_sprites(self.player)
        # List of boolean for already visited checkpoints
        self.has_missed_checkpoint = False
        self.checkpoints_list = []
        for i in range(len(self.map.get_checkpoints())):
            self.checkpoints_list.append(False)

        self.play()

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
        if self.multi:
            self.multi.close_multiplayer()
        ColorCar.remove_temp_files()

    def update_player(self):
        self.verify_checkpoints()
        keys = pygame.key.get_pressed()
        self.player.handle_keys_press(keys)
        if self.player.rect.collidelist(self.map.get_collisions_objects()) != -1:
            self.player.crash()

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
            idx_last_visited_checkpoint = next(x for x, val in enumerate(self.checkpoints_list) if val == False) - 1
            if (not (idx_last_visited_checkpoint == -1) and
                    len(idx_passed) and
                    idx_passed[0] > idx_last_visited_checkpoint and
                    idx_passed[0] == idx_last_visited_checkpoint + 1):
                self.HUD.has_missed_checkpoint = True
        except:
            print("Player have passed all checkpoints")

    def send_player_data(self):
        if self.multi.client:
            player_data = {
                "pos": self.player.rect.center,
                "angle": self.player.angle,
                "speed": self.player.velocity
            }
            self.multi.client.send_player_data(player_data)

    def set_racers(self, racers_data):
        racers = {}
        for racer_data in racers_data:
            db_id = racer_data["db_id"]
            if db_id == self.multi.client.db_id:
                continue
            color_car = ColorCar()
            color_car.set_roof_color(racer_data["colors"]["roof"])
            color_car.set_base_color(racer_data["colors"]["base"])
            imgPath = color_car.save_img(db_id)
            img = pygame.image.load(imgPath).convert_alpha()
            racer = Racer(db_id, racer_data["pseudo"], img, (500, 500))  # racer_data.pos
            racers[db_id] = {"racer": racer}
            racers[db_id]["tag"] = GameTag("test", (500, 500))
        return racers

    def handle_server_data(self):
        res = self.multi.client.receive()
        if not res:
            return
        for protocol, data in res:
            if protocol.value == ClientProtocol.PLAYERS_INFOS.value:
                racers_data = json.loads(data)
                self.racers = self.set_racers(racers_data)
                sprites = ([racer["racer"] for racer in self.racers.values()] +
                           [racer["tag"] for racer in self.racers.values()])
                self.map.add_racers(sprites)
                # add racers to the HUD for pseudo display
            elif protocol.value == ClientProtocol.ACTION.value:
                if data == "Start game":
                    self.is_game_started = True
            elif protocol.value == ClientProtocol.DATA.value:
                players_data = json.loads(data)
                for db_id, player_data in players_data.items():
                    if db_id == self.multi.client.db_id:
                        continue  # Normalement on ne devrait pas recevoir nos propres données
                    self.racers[db_id]["racer"].rect.center = player_data["pos"]
                    self.racers[db_id]["tag"].change_pos(player_data["pos"])
                    self.racers[db_id]["racer"].angle = player_data["angle"]
                    self.racers[db_id]["racer"].velocity = player_data["speed"]
            elif protocol.value == ClientProtocol.ERROR.value:
                print(data)

    def update(self):
        self.update_player()
        if self.multi:
            self.handle_server_data()
            self.send_player_data()

        self.map.update()
        self.HUD.speedometer.speed = self.player.velocity

    def render(self):
        world_surface = self.map.get_world_surface()
        if self.enable_screen_rotation:
            world_surface = pygame.transform.rotozoom(world_surface, -self.player.angle, 1)
        rect = world_surface.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 2))
        self.window.blit(world_surface, rect)
        self.HUD.blit_HUD(self.window, self.checkpoints_list, time.time() - self.start_time)
