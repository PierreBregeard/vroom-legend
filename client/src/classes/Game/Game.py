import time

import pygame
import json

from .User import User
from ..Controler.Parties import ControlerParties
from ..ResourcePath import RelativePath
from .World import World
from ..Sprites.Player import Player
from ..Sprites.Racer import Racer
from ..Sprites.ColorCar import ColorCar
from ..HUD.HUD import HUD
from ..UDP.ClientProtocol import ClientProtocol
from ..Sprites.GameTag import GameTag


class Game:
    is_game_started = False

    def reset(self):
        # Reset all game-related variables and objects
        self.player = self.init_player()
        self.HUD = HUD(self.screen_size, self.player.max_speed)
        self.checkpoints_list = [False] * len(self.map.get_checkpoints())
        # Other game-specific reset logic goes here

    def init_player(self):
        color_car = ColorCar()
        color_car.set_roof_color(tuple(User.color1))
        color_car.set_base_color(tuple(User.color2))
        img_path = color_car.save_img()
        img = pygame.image.load(img_path).convert_alpha()
        return Player(0, img, (self.map.spawnpoints[0][0], self.map.spawnpoints[0][1]), self.map.spawnpoints[0][2])

    def __init__(self, enable_screen_rotation, game_size, multi=None, racers_data=None):
        self.game_is_done = False
        self.multi = multi
        self.enable_screen_rotation = enable_screen_rotation
        self.racers = {}
        self.screen_size = game_size
        self.window = pygame.display.set_mode(self.screen_size)

        # LOAD MAP BEFORE PLAYERS TO GET SPAWNPOINTS
        map_path = RelativePath.resource_path("ressources/Maps/dependencies/FirstMap.tmx")
        self.map = World(map_path, self.screen_size, self.enable_screen_rotation)

        self.cant_rollback = True
        self.start_time = 0
        self.player = self.init_player()

        self.HUD = HUD(self.screen_size, self.player.max_speed)

        self.map.set_soom(1)
        self.map.add_sprites(self.player)
        if self.multi:
            self.set_racers(racers_data)

        # List of boolean for already visited checkpoints
        self.has_missed_checkpoint = False
        self.checkpoints_list = []
        # Coords of the last checkpoint the player has passed
        self.last_checkpoints_coords = None
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
        ColorCar().remove_temp_files()

    def start_game(self):
        self.HUD.info.text_to_show = ""
        self.start_time = time.time()
        self.is_game_started = True

    def update_player(self):
        if self.game_is_done is False:
            self.verify_checkpoints()
        if self.last_checkpoints_coords is not None:
            self.cant_rollback = False

        keys = pygame.key.get_pressed()
        self.player.handle_keys_press(keys)
        self.HUD.cant_rollback = False
        if keys[pygame.K_r]:
            if self.cant_rollback:
                self.HUD.cant_rollback = self.cant_rollback
            elif not self.cant_rollback:
                self.player.rect.x = self.last_checkpoints_coords[0]
                self.player.rect.y = self.last_checkpoints_coords[1]
                self.player.angle = self.last_checkpoints_coords[2]

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
            self.last_checkpoints_coords = (self.player.rect.x, self.player.rect.y, self.player.angle)
        try:
            idx_last_visited_checkpoint = next(x for x, val in enumerate(self.checkpoints_list) if val == False) - 1
            if (not (idx_last_visited_checkpoint == -1) and
                    len(idx_passed) and
                    idx_passed[0] > idx_last_visited_checkpoint and
                    idx_passed[0] == idx_last_visited_checkpoint + 1):
                self.HUD.has_missed_checkpoint = True
        except:
            self.game_is_done = True
            if len(User.pseudo) > 1:
                current_time = time.time()
                data = {"pseudo": User.pseudo, "parties": {"id_map": 1, "type": "solo", "time": current_time}}
                ControlerParties.save_history(data)
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

        def format_racers():
            racers = {}
            spawnpoint = self.map.spawnpoints[0]
            for i, racer_data in enumerate(racers_data):
                db_id = racer_data["db_id"]
                if db_id == self.multi.client.db_id:
                    continue
                color_car = ColorCar()
                color_car.set_roof_color(racer_data["colors"]["roof"])
                color_car.set_base_color(racer_data["colors"]["base"])
                imgPath = color_car.save_img(db_id)
                img = pygame.image.load(imgPath).convert_alpha()
                racer = Racer(db_id, racer_data["pseudo"], img,(spawnpoint[0], spawnpoint[1]) , spawnpoint[2])  # racer_data.pos
                racers[db_id] = {"racer": racer}
                racers[db_id]["tag"] = GameTag(racer_data["pseudo"], (spawnpoint[0], spawnpoint[1]))
            return racers

        self.racers = format_racers()
        sprites = ([racer["racer"] for racer in self.racers.values()] +
                   [racer["tag"] for racer in self.racers.values()])
        self.map.add_racers(sprites)

    def handle_server_data(self):
        res = self.multi.client.receive()
        if not res:
            return
        for protocol, data in res:
            if protocol.value == ClientProtocol.PLAYERS_INFOS.value:
                racers_data = json.loads(data)
                self.set_racers(racers_data)
            elif protocol.value == ClientProtocol.ACTION.value:
                self.HUD.info.text_to_show = data
                if data == "Start game":
                    self.start_game()
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
        if self.is_game_started:
            self.update_player()

        if self.multi:
            self.handle_server_data()
            self.send_player_data()
        elif not self.multi and not self.is_game_started:
            self.start_game()

        self.map.update()
        self.HUD.speedometer.speed = self.player.velocity
        self.HUD.checkpoint_manager.checkpoint_list = self.checkpoints_list
        if self.is_game_started:
            time_to_show = time.time() - self.start_time
        else:
            time_to_show = 0
        self.HUD.timer.time = time_to_show

    def render(self):
        world_surface = self.map.get_world_surface()
        if self.enable_screen_rotation:
            world_surface = pygame.transform.rotozoom(world_surface, -self.player.angle, 1)
        rect = world_surface.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 2))
        self.window.blit(world_surface, rect)
        self.HUD.blit_HUD(self.window)
