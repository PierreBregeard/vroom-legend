import sys
import pygame
import pygame_gui
from .Button import Button
from ..ResourcePath import RelativePath
from ..HUD.Font import Font
from ..Game.Multiplayer import Multiplayer
from ..Game.Game import Game

clock = pygame.time.Clock()


class Hosting:
    def __init__(self, width, height):
        # à voir si on veut changer les variables en fonction de la taille de l'écran du joueur
        self.largeur, self.hauteur = width, height
        self.screen = pygame.display.set_mode((self.largeur, self.hauteur))
        pygame.display.set_caption("Multijoueur")

        main_font = pygame.font.SysFont("cambria", 50)
        self.BG = pygame.image.load(RelativePath.resource_path("ressources/BackgroundMenu/Background.png"))

        self.button_click_sound = pygame.mixer.Sound(RelativePath.resource_path("ressources/Sounds/Minimalist10.mp3"))

        self.BG = pygame.transform.scale(self.BG, (self.largeur, self.hauteur))

        self.menu_text = Font.get_font(70).render("Multijoueur", True, "#FFFFFF")
        self.menu_rect = self.menu_text.get_rect(center=(self.largeur // 2, self.hauteur * 0.8/10))

        # Redéfini la taille du bouton avec le .transform.scale
        self.button_surface = pygame.image.load(RelativePath.resource_path("ressources/Buttons/bouton2red.png"))
        self.button_surface = pygame.transform.scale(self.button_surface, (220, 90))

        self.button_surface2 = pygame.image.load(RelativePath.resource_path("ressources/Buttons/bouton2.png"))
        self.button_surface2 = pygame.transform.scale(self.button_surface2, (150, 100))

        self.manager = pygame_gui.UIManager((self.largeur, self.hauteur))

        self.ip_text = Font.get_font(17).render("IP :", True, "#b68f40")
        self.ip_rect = self.ip_text.get_rect(center=(self.largeur * 3.7/10, self.hauteur * 5.6/10))

        self.wrong_ip_text = Font.get_font(16).render("Veuillez entrer une adresse IP valide!", True, "#ff0000")
        self.wrong_ip_rect = self.wrong_ip_text.get_rect(center=(self.largeur * 5/10, self.hauteur * 7/10))

        self.not_connected_text = Font.get_font(16).render("Vous devez être connecté !", True, "#ff0000")
        self.not_connected_rect = self.not_connected_text.get_rect(center=(self.largeur * 5/10, self.hauteur * 7/10))

        self.wrong_ip = False
        self.not_connected = False

        self.ip_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((self.largeur * 3.25/10, self.hauteur * 6/10),
                                                                                      (self.largeur // 3, 40)),
                                                            manager=self.manager, object_id="#email")

        self.back_button = Button(pos=(self.largeur // 8, self.hauteur * 9/10), text_input="Retour", font=Font.get_font(16),
                                  base_color="#FFFFFF", hovering_color="White", image=self.button_surface2)

        self.join_button = Button(pos=(self.largeur // 2, self.hauteur * 7.8/10), text_input="Rejoindre", font=Font.get_font(17),
                                   base_color="#ffffff", hovering_color="White", image=self.button_surface)

        self.host_button = Button(pos=(self.largeur // 2, self.hauteur * 4/10), text_input="Héberger", font=Font.get_font(17),
                                   base_color="#ffffff", hovering_color="White", image=self.button_surface)

        self.run = True

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

            for button in [self.back_button, self.join_button, self.host_button]:
                button.changecolor(mouse_pos)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.checkinput(mouse_pos):  # retour menu
                        self.button_click_sound.play()
                        return
                    if self.join_button.checkinput(mouse_pos):  # retour menu attente joueur
                        self.button_click_sound.play()
                        # todo: vérifier si il est co pour faire ça
                        # if ...:
                            # self.not_connected = True
                        if ip_len < 5:
                            self.wrong_ip = True
                        else:
                            self.wrong_ip = False
                        if not self.wrong_ip:
                            multi = Multiplayer(is_server=False, addr=self.ip_input.get_text())
                            Game(game_size=(self.largeur, self.hauteur), enable_screen_rotation=False).play(multi)
                            return
                    if self.host_button.checkinput(mouse_pos):  # retour menu attente joueur
                        self.button_click_sound.play()
                        multi = Multiplayer(is_server=True)
                        Game(game_size=(self.largeur, self.hauteur), enable_screen_rotation=False).play(multi)
                        return

                self.manager.process_events(event)

            self.manager.update(fps)

            self.manager.draw_ui(self.screen)

            pygame.display.update()
