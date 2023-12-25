import pygame
import sys
from src.classes.Menu.button import Button
from src.classes.Game.Game import Game


def get_font(size):
    return pygame.font.Font("./ressources/Font/Roboto-Black.ttf", size)


class Menu:
    def __init__(self, width=600, height=600):
        pygame.init()
        # à voir si on veut changer les variables en fonction de la taille de l'écran du joueur
        self.largeur, self.hauteur = 1000, 720
        self.screen = pygame.display.set_mode((self.largeur, self.hauteur))
        pygame.display.set_caption("Menu")

        main_font = pygame.font.SysFont("cambria", 50)
        self.BG = pygame.image.load("./ressources/BackgroundMenu/Background.png")
        self.BG = pygame.transform.scale(self.BG, (self.largeur, self.hauteur))

        # Redéfini la taille du bouton avec le .transform.scale
        self.button_surface = pygame.image.load("./ressources/Buttons/bouton1.png")
        self.button_surface = pygame.transform.scale(self.button_surface, (150, 85))
        self.run = True
        self.run_game = Game()
        self.screen.blit(self.BG, (0, 0))

        self.menu_text = get_font(80).render("Vroom Legends", True, "#b68f40")
        self.menu_rect = self.menu_text.get_rect(center=(350, 100))

        self.play_button = Button(pos=(350, 225), text_input="Jouer", font=get_font(30),
                                  base_color="#d7fcd4", hovering_color="White", image=self.button_surface)

        self.connexion_button = Button(pos=(350, 335), text_input="Connexion",
                                       font=get_font(25),
                                       base_color="#d7fcd4", hovering_color="White", image=self.button_surface)

        self.leave_button = Button(pos=(350, 450), text_input="Quitter", font=get_font(30),
                                   base_color="#d7fcd4", hovering_color="White", image=self.button_surface)

    def menu(self, game):  # enlever le parametre game quand la classe sera op
        while self.run:
            self.screen.blit(self.BG, (0, 0))

            mouse_pos = pygame.mouse.get_pos()

            self.screen.blit(self.menu_text, self.menu_rect)

            for button in [self.play_button, self.connexion_button, self.leave_button]:
                button.changecolor(mouse_pos)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_button.checkinput(mouse_pos):
                        game.play()
                        self.run = False
                    # if connexion_button.checkinput(mouse_pos):
                        # menu_co.menu_co()
                    if self.leave_button.checkinput(mouse_pos):
                        pygame.quit()
                        sys.exit()
            pygame.display.update()
