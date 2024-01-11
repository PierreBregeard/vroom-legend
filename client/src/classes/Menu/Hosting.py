import sys
import pygame
import pygame_gui
from .Button import Button
from ..ResourcePath import RelativePath
from ..HUD.Font import Font
from ..Game.Multiplayer import Multiplayer
from ..Game.Game import Game
from .WaitingRoom import WaitingRoom

clock = pygame.time.Clock()


class Hosting:
    def __init__(self, width, height):
        self.largeur, self.hauteur = width, height
        self.screen = pygame.display.set_mode((self.largeur, self.hauteur))
        pygame.display.set_caption("Multijoueur")

        self.BG = pygame.image.load(RelativePath.resource_path("ressources/BackgroundMenu/Background.png"))

        self.button_click_sound = pygame.mixer.Sound(RelativePath.resource_path("ressources/Sounds/Minimalist10.mp3"))

        self.BG = pygame.transform.scale(self.BG, (self.largeur, self.hauteur))

        self.menu_text = Font.get_font(self.largeur * 1 // 15).render("Multijoueur", True, "#FFFFFF")
        self.menu_rect = self.menu_text.get_rect(center=(self.largeur // 2, self.hauteur * 1/11))

        self.button_surface = pygame.image.load(RelativePath.resource_path("ressources/Buttons/bouton2red.png"))
        self.button_surface = pygame.transform.scale(self.button_surface, (self.largeur * 2/9, self.hauteur * 1/11))

        self.button_surface2 = pygame.image.load(RelativePath.resource_path("ressources/Buttons/bouton2.png"))
        self.button_surface2 = pygame.transform.scale(self.button_surface2, (self.largeur * 1/5, self.hauteur * 1/10))

        self.manager = pygame_gui.UIManager((self.largeur, self.hauteur))

        self.ip_text = Font.get_font(17).render("IP :", True, "#b68f40")
        self.ip_rect = self.ip_text.get_rect(center=(self.largeur * 4/10, self.hauteur * 6/11))

        self.wrong_ip_text = Font.get_font(16).render("Veuillez entrer une adresse IP valide!", True, "#ff0000")
        self.wrong_ip_rect = self.wrong_ip_text.get_rect(center=(self.largeur * 5/10, self.hauteur * 7/10))

        self.wrong_ip_text2 = Font.get_font(16).render("Le serveur n'a pas été trouvé !", True, "#ff0000")
        self.wrong_ip_rect2 = self.wrong_ip_text2.get_rect(center=(self.largeur * 5/10, self.hauteur * 7/10))

        self.not_connected_text = Font.get_font(16).render("Vous devez être connecté !", True, "#ff0000")
        self.not_connected_rect = self.not_connected_text.get_rect(center=(self.largeur * 5/10, self.hauteur * 7/10))

        self.wrong_ip = False
        self.wrong_ip2 = False
        self.not_connected = False

        self.ip_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((self.largeur * 4/11, self.hauteur * 6/10),
                                                                                      (self.largeur // 3, 40)),
                                                            manager=self.manager, object_id="#email")

        self.back_button = Button(pos=(self.largeur // 8, self.hauteur * 9/10), text_input="Retour", font=Font.get_font(self.largeur * 1//55),
                                  base_color="#FFFFFF", hovering_color="White", image=self.button_surface2)

        self.join_button = Button(pos=(self.largeur // 2, self.hauteur * 8/10), text_input="Rejoindre", font=Font.get_font(self.largeur * 1//55),
                                   base_color="#ffffff", hovering_color="White", image=self.button_surface)

        self.host_button = Button(pos=(self.largeur // 2, self.hauteur * 4/10), text_input="Héberger", font=Font.get_font(self.largeur * 1//55),
                                   base_color="#ffffff", hovering_color="White", image=self.button_surface)

        self.run = True

        self.waiting = WaitingRoom(self.largeur, self.hauteur)

        self.disable_button = False

        clock.tick(60)
        pygame.display.update()

    def menu_multi(self):
        while self.run:
            fps = clock.tick(60) / 1000
            mouse_pos = pygame.mouse.get_pos()

            ip_len = len(self.ip_input.get_text())

            self.screen.blit(self.BG, (0, 0))
            self.screen.blit(self.menu_text, self.menu_rect)
            self.screen.blit(self.ip_text, self.ip_rect)

            if self.wrong_ip:
                self.screen.blit(self.wrong_ip_text, self.wrong_ip_rect)
            if self.not_connected:
                self.screen.blit(self.not_connected_text, self.not_connected_rect)
            if self.wrong_ip2:
                self.screen.blit(self.wrong_ip_text2, self.wrong_ip_rect2)

            for button in [self.back_button, self.join_button, self.host_button]:
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
                    if not self.disable_button and self.join_button.checkinput(mouse_pos):
                        self.disable_button = True
                        self.button_click_sound.play()
                        self.wrong_ip = ip_len < 5
                        if not self.wrong_ip:
                            multi = Multiplayer(is_server=False, addr=self.ip_input.get_text())
                            if not multi.client:
                                self.wrong_ip = False
                                self.wrong_ip2 = True
                            else:
                                self.waiting.menu_wait("Join", multi)
                                return
                        self.disable_button = False
                    if self.host_button.checkinput(mouse_pos):
                        self.button_click_sound.play()
                        multi = Multiplayer(is_server=True)
                        self.waiting.menu_wait("Host", multi)
                        return

                self.manager.process_events(event)

            self.manager.update(fps)

            self.manager.draw_ui(self.screen)

            pygame.display.update()
