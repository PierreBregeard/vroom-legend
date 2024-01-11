import pygame
import sys
from .Button import Button
from .Connexion import Connexion
from .History import History
from .Custom import Custom
from .Hosting import Hosting
from ..Game.Game import Game
from ..Game.User import User
from ..ResourcePath import RelativePath
from ..HUD.Font import Font


class Menu:

    def __init__(self, game_size):
        self.largeur, self.hauteur = game_size
        self.screen = pygame.display.set_mode((self.largeur, self.hauteur))
        pygame.display.set_caption("Vroom Legends")

        self.BG = pygame.image.load(RelativePath.resource_path("ressources/BackgroundMenu/Background2.png"))

        self.BG = pygame.transform.scale(self.BG, (self.largeur, self.hauteur))

        self.button_click_sound = pygame.mixer.Sound(RelativePath.resource_path("ressources/Sounds/Minimalist10.mp3"))

        self.button_surface = pygame.image.load(RelativePath.resource_path("ressources/Buttons/bouton2.png"))
        self.button_surface = pygame.transform.scale(self.button_surface, (self.largeur * 1/3, self.hauteur * 1/10))

        self.button_surface2 = pygame.image.load(RelativePath.resource_path("ressources/Buttons/bouton2red.png"))
        self.button_surface2 = pygame.transform.scale(self.button_surface2, (self.largeur * 1/3, self.hauteur * 1/10))

        self.run = True

        self.screen.blit(self.BG, (0, 0))

        self.menu_text = Font.get_font(self.largeur * 1 // 15).render("Vroom Legends", True, "#d7fcd4")
        self.menu_rect = self.menu_text.get_rect(center=(self.largeur // 2, self.hauteur * 1 // 10))

        self.play_button = Button(pos=(self.largeur // 2, self.hauteur * 3/10), text_input="Solo", font=Font.get_font(self.largeur * 1//49),
                                  base_color="#d7fcd4", hovering_color="White", image=self.button_surface)

        self.multiplayer_button = Button(pos=(self.largeur // 2, self.hauteur * 4/10), text_input="Multijoueur", font=Font.get_font(self.largeur * 1//49),
                                         base_color="#d7fcd4", hovering_color="White", image=self.button_surface)

        self.connexion_button = Button(pos=(self.largeur // 2, self.hauteur * 5/10), text_input="Connexion",
                                       font=Font.get_font(self.largeur * 1//49),
                                       base_color="#d7fcd4", hovering_color="White", image=self.button_surface)

        self.customisation_button = Button(pos=(self.largeur // 2, self.hauteur * 6/10), text_input="Customisation",
                                           font=Font.get_font(self.largeur * 1//49),
                                           base_color="#d7fcd4", hovering_color="White", image=self.button_surface)

        self.leave_button = Button(pos=(self.largeur // 2, self.hauteur * 7/10), text_input="Quitter", font=Font.get_font(self.largeur * 1//49),
                                   base_color="#d7fcd4", hovering_color="White", image=self.button_surface)

        self.history_button = Button(pos=(self.largeur * 2 / 11, self.hauteur * 12 / 13), text_input="Historique",
                                  font=Font.get_font(self.largeur * 1 // 55),
                                  base_color="#FFFFFF", hovering_color="White", image=self.button_surface)

        self.deco_button = Button(pos=(self.largeur * 9 / 11, self.hauteur * 12 / 13), text_input="Déconnexion",
                                  font=Font.get_font(self.largeur * 1 // 55),
                                  base_color="#FFFFFF", hovering_color="White", image=self.button_surface2)

        self.pseudo = User.pseudo
        self.pseudo_text = Font.get_font(self.largeur * 1 // 40).render(f"Bonjour {self.pseudo}", True, "#FFFFFF")
        self.pseudo_rect = self.pseudo_text.get_rect(
            center=(self.largeur // 2, self.hauteur * 2/11))

    def menu(self):
        while self.run:
            self.screen.blit(self.BG, (0, 0))
            if len(User.pseudo) > 1:
                self.screen.blit(self.pseudo_text, self.pseudo_rect)

            mouse_pos = pygame.mouse.get_pos()

            self.screen.blit(self.menu_text, self.menu_rect)

            if len(User.pseudo) > 1:
                self.deco_button.changecolor(mouse_pos)
                self.deco_button.update(self.screen)
                self.history_button.changecolor(mouse_pos)
                self.history_button.update(self.screen)

            for button in [self.play_button, self.connexion_button, self.leave_button, self.customisation_button,
                           self.multiplayer_button]:
                button.changecolor(mouse_pos)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button != 1:
                        continue
                    if self.play_button.checkinput(mouse_pos):
                        self.button_click_sound.play()
                        Game(game_size=(self.largeur, self.hauteur), enable_screen_rotation=False)
                    if self.history_button.checkinput(mouse_pos):
                        history = History(self.largeur, self.hauteur)
                        history.menu_history()
                    if self.connexion_button.checkinput(mouse_pos):
                        self.button_click_sound.play()
                        menu = Connexion(self.largeur, self.hauteur)
                        menu.menu_co()
                        test_menu = Menu(game_size=(self.largeur, self.hauteur))
                        test_menu.menu()

                    if self.multiplayer_button.checkinput(mouse_pos):
                        self.button_click_sound.play()
                        menu = Hosting(self.largeur, self.hauteur)
                        menu.menu_multi()

                    if self.customisation_button.checkinput(mouse_pos):
                        self.button_click_sound.play()
                        menu = Custom(self.largeur, self.hauteur)
                        menu.menu_custom()

                    if self.leave_button.checkinput(mouse_pos):
                        self.button_click_sound.play()
                        pygame.quit()
                        sys.exit()

                    if self.deco_button.checkinput(mouse_pos):
                        self.button_click_sound.play()
                        User.pseudo = ""
                        User.color1 = (100, 0, 0)
                        User.color2 = (0, 100, 0)
                        return

            pygame.display.update()
