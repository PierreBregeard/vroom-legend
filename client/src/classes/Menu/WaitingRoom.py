import sys
import pygame
import pygame_gui
from .Button import Button
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
        # à voir si on veut changer les variables en fonction de la taille de l'écran du joueur
        self.largeur, self.hauteur = width, height
        self.screen = pygame.display.set_mode((self.largeur, self.hauteur))
        pygame.display.set_caption("Waiting Room")

        main_font = pygame.font.SysFont("cambria", 50)
        self.BG = pygame.image.load(RelativePath.resource_path("ressources/BackgroundMenu/Background.png"))

        self.button_click_sound = pygame.mixer.Sound(RelativePath.resource_path("ressources/Sounds/Minimalist10.mp3"))

        self.BG = pygame.transform.scale(self.BG, (self.largeur, self.hauteur))

        self.menu_text = Font.get_font(self.largeur * 1 // 15).render("Waiting Room", True, "#FFFFFF")
        self.menu_rect = self.menu_text.get_rect(center=(self.largeur // 2, self.hauteur * 1 / 10))

        self.list_text = Font.get_font(self.largeur * 1 // 70).render("Joueurs :", True, "#FFFFFF")
        self.list_rect = self.list_text.get_rect(center=(self.largeur * 2 / 10, self.hauteur * 2 / 10))

        # Redéfini la taille du bouton avec le .transform.scale
        self.button_surface = pygame.image.load(RelativePath.resource_path("ressources/Buttons/bouton2red.png"))
        self.button_surface = pygame.transform.scale(self.button_surface, (220, 90))

        self.button_surface2 = pygame.image.load(RelativePath.resource_path("ressources/Buttons/bouton2.png"))
        self.button_surface2 = pygame.transform.scale(self.button_surface2, (150, 100))

        self.manager = pygame_gui.UIManager((self.largeur, self.hauteur))

        self.back_button = Button(pos=(self.largeur // 8, self.hauteur * 9 / 10), text_input="Retour",
                                  font=Font.get_font(16),
                                  base_color="#FFFFFF", hovering_color="White", image=self.button_surface2)

        self.start_button = Button(pos=(self.largeur * 8 / 10, self.hauteur * 9 / 10), text_input="Start",
                                   font=Font.get_font(16),
                                   base_color="#FFFFFF", hovering_color="White", image=self.button_surface)

        self.run = True

        self.racers_data = {}

        clock.tick(60)
        pygame.display.update()

    def menu_wait(self, role, multi):
        while self.run:
            fps = clock.tick(60) / 1000
            mouse_pos = pygame.mouse.get_pos()

            self.screen.blit(self.BG, (0, 0))
            self.screen.blit(self.menu_text, self.menu_rect)
            self.screen.blit(self.list_text, self.list_rect)

            if role == "Host":
                self.start_button.changecolor(mouse_pos)
                self.start_button.update(self.screen)

            start_game = False

            # tmp
            color_car = ColorCar()
            color_car.set_roof_color((100, 0, 0))
            color_car.set_base_color((100, 100, 0))

            multi.client.register("Pierre", color_car)  # todo: recup from eva
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
                    if self.back_button.checkinput(mouse_pos):  # retour menu
                        self.button_click_sound.play()
                        return
                    if self.start_button.checkinput(mouse_pos):  # start
                        self.button_click_sound.play()
                        multi.client.send(ServerProtocol.START_GAME.value, "")

                self.manager.process_events(event)

            self.manager.update(fps)

            self.manager.draw_ui(self.screen)

            pygame.display.update()
