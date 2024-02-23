import sys
import pygame
import pygame_gui
from .Button import Button
from ..Game.User import User
from ..ResourcePath import RelativePath
from ..HUD.Font import Font
from ..UDP.ServerProtocol import ServerProtocol
from ..UDP.ClientProtocol import ClientProtocol
from ..Game.Game import Game
from ..Sprites.ColorCar import ColorCar
import json

clock = pygame.time.Clock()


class WaitingRoom:
    def __init__(self, width, height):
        self.largeur, self.hauteur = width, height
        self.screen = pygame.display.set_mode((self.largeur, self.hauteur))
        pygame.display.set_caption("Waiting Room")

        self.BG = pygame.image.load(RelativePath.resource_path("ressources/BackgroundMenu/Background.png"))

        self.button_click_sound = pygame.mixer.Sound(RelativePath.resource_path("ressources/Sounds/Minimalist10.mp3"))

        self.BG = pygame.transform.scale(self.BG, (self.largeur, self.hauteur))

        self.menu_text = Font.get_font(self.largeur * 1 // 15).render("Waiting Room", True, "#FFFFFF")
        self.menu_rect = self.menu_text.get_rect(center=(self.largeur // 2, self.hauteur * 1/11))

        self.list_text = Font.get_font(self.largeur * 1 // 70).render("Joueurs :", True, "#FFFFFF")
        self.list_rect = self.list_text.get_rect(center=(self.largeur * 2 / 10, self.hauteur * 2 / 10))

        self.button_surface = pygame.image.load(RelativePath.resource_path("ressources/Buttons/bouton2red.png"))
        self.button_surface = pygame.transform.scale(self.button_surface, (self.largeur * 2/9, self.hauteur * 1/11))

        self.button_surface2 = pygame.image.load(RelativePath.resource_path("ressources/Buttons/bouton2.png"))
        self.button_surface2 = pygame.transform.scale(self.button_surface2, (self.largeur * 1/5, self.hauteur * 1/10))

        self.manager = pygame_gui.UIManager((self.largeur, self.hauteur))

        self.back_button = Button(pos=(self.largeur // 8, self.hauteur * 9 / 10), text_input="Retour",
                                  font=Font.get_font(self.largeur * 1//55),
                                  base_color="#FFFFFF", hovering_color="White", image=self.button_surface2)

        self.start_button = Button(pos=(self.largeur * 8 / 10, self.hauteur * 9 / 10), text_input="Start",
                                   font=Font.get_font(self.largeur * 1//55),
                                   base_color="#FFFFFF", hovering_color="White", image=self.button_surface)

        self.run = True

        self.racers_data = {}

        clock.tick(60)
        pygame.display.update()

        self.max_players = 4

    def menu_wait(self, role, multi):
        while self.run:

            ip_text = Font.get_font(self.largeur * 1 // 70).render(f"IP : {multi.addr}", True, "#FFFFFF")
            ip_rect = ip_text.get_rect(center=(self.largeur * 7 / 10, self.hauteur * 2 / 10))

            fps = clock.tick(60) / 1000
            mouse_pos = pygame.mouse.get_pos()

            self.screen.blit(self.BG, (0, 0))
            self.screen.blit(self.menu_text, self.menu_rect)
            self.screen.blit(self.list_text, self.list_rect)

            if role == "Host":
                self.start_button.changecolor(mouse_pos)
                self.start_button.update(self.screen)
                self.screen.blit(ip_text, ip_rect)

            start_game = False

            y_offset = self.hauteur * 2 / 10
            connected_players = 0

            anonymous_count = 1

            for racer in self.racers_data:
                if racer["pseudo"]:
                    pseudo = racer["pseudo"]
                else:
                    pseudo = f"Anonyme {anonymous_count}"
                    anonymous_count += 1

                player_text = Font.get_font(self.largeur * 1 // 70).render(pseudo, True, "#FFFFFF")
                player_rect = player_text.get_rect(center=(self.largeur * 4 / 10, y_offset))
                self.screen.blit(player_text, player_rect)
                y_offset += self.hauteur * 1 / 20
                connected_players += 1

            # tmp
            color_car = ColorCar()
            color_car.set_roof_color(tuple(User.color1))
            color_car.set_base_color(tuple(User.color2))
            pseudo = User.pseudo
            multi.client.register(pseudo, color_car)
            res = multi.client.receive()
            if res:
                for protocol, data in res:
                    if protocol.value == ClientProtocol.PLAYERS_INFOS.value:
                        self.racers_data = json.loads(data)
                    elif protocol.value == ClientProtocol.START_GAME.value:
                        start_game = True
            if start_game:
                Game(False, game_size=(self.largeur, self.hauteur), multi=multi, racers_data=self.racers_data)
                return

            for button in [self.back_button]:
                button.changecolor(mouse_pos)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button != 1:
                        continue
                    if self.back_button.checkinput(mouse_pos):
                        self.button_click_sound.play()
                        return
                    if self.start_button.checkinput(mouse_pos):
                        self.button_click_sound.play()
                        multi.client.send(ServerProtocol.START_GAME.value, "")

                self.manager.process_events(event)

            self.manager.update(fps)

            self.manager.draw_ui(self.screen)

            pygame.display.update()
