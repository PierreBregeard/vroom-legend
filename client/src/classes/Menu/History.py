import pygame

from ..Controler.Parties import ControlerParties
from ..Game.User import User
from ..ResourcePath import RelativePath
from .Button import Button
from ..HUD.Font import Font

class History:
    def __init__(self, width, height):
        self.largeur = width
        self.hauteur = height
        self.screen = pygame.display.set_mode((self.largeur, self.hauteur))
        pygame.display.set_caption("Connexion")
        self.run = True
        self.button_click_sound = pygame.mixer.Sound(RelativePath.resource_path("ressources/Sounds/Minimalist10.mp3"))

        self.BG = pygame.image.load(RelativePath.resource_path("ressources/BackgroundMenu/Background.png"))

        # Redéfini la taille du bouton avec le .transform.scale
        self.button_surface = pygame.image.load(RelativePath.resource_path("ressources/Buttons/bouton2.png"))
        self.button_surface = pygame.transform.scale(self.button_surface, (200, 100))
        self.back_button = Button(pos=(self.largeur // 8, self.hauteur * 9 / 10), text_input="Retour",
                                  font=Font.get_font(18),
                                  base_color="#d7fcd4", hovering_color="White", image=self.button_surface)



    def menu_history(self):
        data = {"pseudo" : User.pseudo}
        allparties = ControlerParties.get_parties(data)
        print(allparties)
        while self.run:
            self.screen.blit(self.BG, (0, 0))







