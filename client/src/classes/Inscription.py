import sys
import pygame
import pygame_gui
from src.classes.button import Button
from src.classes.get_font import get_font


class Inscription:
    def __init__(self):
        pygame.init()
        # à voir si on veut changer les variables en fonction de la taille de l'écran du joueur
        self.largeur, self.hauteur = 1000, 720
        self.screen = pygame.display.set_mode((self.largeur, self.hauteur))
        pygame.display.set_caption("Inscription")
        self.screen.fill("black")
        self.mouse_pos = pygame.mouse.get_pos()

        main_font = pygame.font.SysFont("cambria", 50)
        self.BG = pygame.image.load("./ressources/BackgroundMenu/Background.png")

        # Redéfini la taille du bouton avec le .transform.scale
        self.button_surface = pygame.image.load("./ressources/Buttons/bouton1.png")
        self.button_surface = pygame.transform.scale(self.button_surface, (150, 100))
        self.run = True

    def menu_inscription(self):
        while self.run:
            self.screen.blit(self.BG, (0, 0))
            mouse_pos = pygame.mouse.get_pos()
