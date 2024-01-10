import pygame
import sys
from .Button import Button
from .Connexion import Connexion
from .Custom import Custom
from .Multiplayer import Multiplayer
from src.classes.ResourcePath import RelativePath


class Menu:

    @staticmethod
    def get_font(size):
        return pygame.font.Font(RelativePath.resource_path("ressources/Font/Pixel.ttf"), size)

    def __init__(self, game_size):
        # à voir si on veut changer les variables en fonction de la taille de l'écran du joueur
        self.largeur, self.hauteur = game_size
        self.screen = pygame.display.set_mode((self.largeur, self.hauteur))
        pygame.display.set_caption("Menu principal")

        main_font = pygame.font.SysFont("cambria", 50)
        self.BG = pygame.image.load(RelativePath.resource_path("ressources/BackgroundMenu/Background2.png"))

        self.BG = pygame.transform.scale(self.BG, (self.largeur, self.hauteur))

        self.button_click_sound = pygame.mixer.Sound(RelativePath.resource_path("ressources/Sounds/Minimalist10.mp3"))

        # Redéfini la taille du bouton avec le .transform.scale
        self.button_surface = pygame.image.load(RelativePath.resource_path("ressources/Buttons/bouton2.png"))
        self.button_surface = pygame.transform.scale(self.button_surface, (330, 100))
        self.run = True

        self.screen.blit(self.BG, (0, 0))

        self.menu_text = Menu.get_font(70).render("Vroom Legends", True, "#d7fcd4")
        self.menu_rect = self.menu_text.get_rect(center=(self.largeur // 2, 100))

        self.play_button = Button(pos=(self.largeur // 2, self.hauteur * 3/10), text_input="Solo", font=self.get_font(20),
                                  base_color="#d7fcd4", hovering_color="White", image=self.button_surface)

        self.multiplayer_button = Button(pos=(self.largeur // 2, self.hauteur * 4/10), text_input="Multijoueur", font=self.get_font(20),
                                         base_color="#d7fcd4", hovering_color="White", image=self.button_surface)

        self.connexion_button = Button(pos=(self.largeur // 2, self.hauteur * 5/10), text_input="Connexion",
                                       font=self.get_font(20),
                                       base_color="#d7fcd4", hovering_color="White", image=self.button_surface)

        # self.inscription_button = Button(pos=(750, 560), text_input="Inscription",
        #                                  font=self.get_font(20),
        #                                  base_color="#d7fcd4", hovering_color="White", image=self.button_surface)

        self.customisation_button = Button(pos=(self.largeur // 2, self.hauteur * 6/10), text_input="Customisation",
                                           font=self.get_font(20),
                                           base_color="#d7fcd4", hovering_color="White", image=self.button_surface)

        self.leave_button = Button(pos=(self.largeur // 2, self.hauteur * 7/10), text_input="Quitter", font=self.get_font(20),
                                   base_color="#d7fcd4", hovering_color="White", image=self.button_surface)

    def menu(self, game):
        while self.run:
            self.screen.blit(self.BG, (0, 0))

            mouse_pos = pygame.mouse.get_pos()

            self.screen.blit(self.menu_text, self.menu_rect)

            for button in [self.play_button, self.connexion_button, self.leave_button, self.customisation_button, self.multiplayer_button]:
                button.changecolor(mouse_pos)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_button.checkinput(mouse_pos):
                        self.button_click_sound.play()
                        print("Jeu")
                        game.play()

                    if self.connexion_button.checkinput(mouse_pos):
                        self.button_click_sound.play()
                        menu = Connexion(self.largeur, self.hauteur)
                        menu.menu_co()

                    if self.multiplayer_button.checkinput(mouse_pos):
                        self.button_click_sound.play()
                        menu = Multiplayer(self.largeur, self.hauteur)
                        menu.menu_multi()

                    if self.customisation_button.checkinput(mouse_pos):
                        self.button_click_sound.play()
                        menu = Custom(self.largeur, self.hauteur)
                        menu.menu_custom()

                    if self.leave_button.checkinput(mouse_pos):
                        self.button_click_sound.play()
                        pygame.quit()
                        sys.exit()

            pygame.display.update()
