import sys
import pygame
import pygame_gui
import re
from .Button import Button
from ..Controler.Log import Log
from ..ResourcePath import RelativePath
from ..HUD.Font import Font

import requests


# from src.main import init_menu
# from src.classes.Inscription import Inscription


def get_font(size):
    return pygame.font.Font(RelativePath.resource_path("ressources/Font/Pixel.ttf"), size)


def is_valid_email(email):
    email_pattern = re.compile(r'^[\w.-]+@[a-zA-Z\d.-]+\.[a-zA-Z]{2,}$')
    return bool(re.match(email_pattern, email))


clock = pygame.time.Clock()


class Inscription:
    def __init__(self, width, height):
        self.largeur, self.hauteur = width, height
        self.screen = pygame.display.set_mode((self.largeur, self.hauteur))
        pygame.display.set_caption("Inscription")

        self.BG = pygame.image.load(RelativePath.resource_path("ressources/BackgroundMenu/Background.png"))

        self.BG = pygame.transform.scale(self.BG, (self.largeur, self.hauteur))

        self.button_click_sound = pygame.mixer.Sound(RelativePath.resource_path("ressources/Sounds/Minimalist10.mp3"))

        self.menu_text = Font.get_font(self.largeur * 1//15).render("Inscription", True, "#FFFFFF")
        self.menu_rect = self.menu_text.get_rect(center=(self.largeur // 2, self.hauteur * 1/10))

        self.pseudo_text = Font.get_font(self.largeur * 1//58).render("Pseudo :", True, "#b68f40")
        self.pseudo_rect = self.pseudo_text.get_rect(center=(self.largeur // 7, self.hauteur * 2/11))

        self.email_text = Font.get_font(self.largeur * 1//58).render("Email : ", True, "#b68f40")
        self.email_rect = self.email_text.get_rect(center=(self.largeur // 7, self.hauteur * 5/15))

        self.mdp_text = Font.get_font(self.largeur * 1//58).render("Mot de passe :", True, "#b68f40")
        self.mdp_rect = self.mdp_text.get_rect(center=(self.largeur // 5, self.hauteur * 10/21))

        self.conf_mdp_text = Font.get_font(self.largeur * 1//58).render("Confirmez :", True, "#b68f40")
        self.conf_mdp_rect = self.conf_mdp_text.get_rect(center=(self.largeur * 2/12, self.hauteur * 10/16))

        self.wrong_pseudo_text = Font.get_font(self.largeur * 1//58).render("Veuillez entrer un pseudo de plus de 3 caractères !", True, "#ff0000")
        self.wrong_pseudo_rect = self.wrong_pseudo_text.get_rect(center=(self.largeur // 2, self.hauteur * 3/11))

        self.wrong_email_text = Font.get_font(self.largeur * 1//58).render("Veuillez entrer un email correct !", True, "#ff0000")
        self.wrong_email_rect = self.wrong_email_text.get_rect(center=(self.largeur * 4/11, self.hauteur * 6/14))

        self.wrong_mdp_text = Font.get_font(self.largeur * 1//58).render("Votre mot de passe doit faire au moins 8 caractères !", True, "#ff0000")
        self.wrong_mdp_rect = self.wrong_mdp_text.get_rect(center=(self.largeur // 2, self.hauteur * 7/12))

        self.wrong_conf_mdp_text = Font.get_font(self.largeur * 1//58).render("Vos mots de passes doivent être identiques !", True, "#ff0000")
        self.wrong_conf_mdp_rect = self.wrong_conf_mdp_text.get_rect(center=(self.largeur * 6/14, self.hauteur * 7/10))

        self.wrong_email = False
        self.wrong_pseudo = False
        self.wrong_mdp = False
        self.wrong_conf_mdp = False

        # Redéfini la taille du bouton avec le .transform.scale
        self.button_surface = pygame.image.load(RelativePath.resource_path("ressources/Buttons/bouton2.png"))
        self.button_surface = pygame.transform.scale(self.button_surface, (self.largeur * 1/5, self.hauteur * 1/10))

        self.button_surface2 = pygame.image.load(RelativePath.resource_path("ressources/Buttons/bouton2red.png"))
        self.button_surface2 = pygame.transform.scale(self.button_surface2, (self.largeur * 2/9, self.hauteur * 1/11))

        self.manager = pygame_gui.UIManager((self.largeur, self.hauteur))


        self.pseudo_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((self.largeur // 15, self.hauteur * 2/10), (self.largeur * 5/10, 40)),
                                                                manager=self.manager, object_id="#pseudonyme")

        self.email_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((self.largeur // 15, self.hauteur * 4/11), (self.largeur * 5/10, 40)),
                                                               manager=self.manager, object_id="#email")

        self.mdp_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((self.largeur // 15, self.hauteur * 5/10), (self.largeur * 5/10, 40)),
                                                             manager=self.manager, object_id="#mot_de_passe")

        self.mdp_input.set_text_hidden(True)

        self.conf_mdp_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((self.largeur // 15, self.hauteur * 9/14), (self.largeur * 5/10, 40)),
                                                                  manager=self.manager, object_id="#conf_mot_de_passe")

        self.conf_mdp_input.set_text_hidden(True)

        self.connexion_txt = Button(pos=(self.largeur // 2, self.hauteur * 9/11), text_input="Vous avez déjà un compte ? Cliquez ici !",
                                    font=Font.get_font(self.largeur * 1//55),
                                    base_color="#d7fcd4", hovering_color="White")

        self.enter_button = Button(pos=(self.largeur // 2, self.hauteur * 10/13), text_input="S'inscrire", font=Font.get_font(self.largeur * 1//55),
                                   base_color="#ffffff", hovering_color="White", image=self.button_surface2)

        self.back_button = Button(pos=(self.largeur // 8, self.hauteur * 9/10), text_input="Retour", font=Font.get_font(self.largeur * 1//55),
                                  base_color="#d7fcd4", hovering_color="White", image=self.button_surface)

        self.run = True

        clock.tick(60)
        pygame.display.update()

    def menu_inscr(self):
        while self.run:
            fps = clock.tick(60) / 1000

            pseudo_len = len(self.pseudo_input.get_text())
            mdp_len = len(self.mdp_input.get_text())

            data = {
                "email": self.email_input.get_text(),
                "pseudo": self.pseudo_input.get_text(),
                "mdp": self.mdp_input.get_text()
            }

            self.screen.blit(self.BG, (0, 0))

            mouse_pos = pygame.mouse.get_pos()

            # affiche les text

            self.screen.blit(self.menu_text, self.menu_rect)
            self.screen.blit(self.email_text, self.email_rect)
            self.screen.blit(self.pseudo_text, self.pseudo_rect)
            self.screen.blit(self.mdp_text, self.mdp_rect)
            self.screen.blit(self.conf_mdp_text, self.conf_mdp_rect)

            # affiche les messages d'erreurs, ne pas toucher

            if self.wrong_email:
                self.screen.blit(self.wrong_email_text, self.wrong_email_rect)
            if self.wrong_pseudo:
                self.screen.blit(self.wrong_pseudo_text, self.wrong_pseudo_rect)
            if self.wrong_mdp:
                self.screen.blit(self.wrong_mdp_text, self.wrong_mdp_rect)
            if self.wrong_conf_mdp:
                self.screen.blit(self.wrong_conf_mdp_text, self.wrong_conf_mdp_rect)

            for button in [self.enter_button, self.back_button, self.connexion_txt]:  # pas toucher
                button.changecolor(mouse_pos)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:  # quand tu clique sur l'écran
                    if event.button != 1:
                        continue
                    if self.enter_button.checkinput(mouse_pos):  # Quand l'utilisateur essaye s'inscrire par bouton
                        self.button_click_sound.play()
                        if mdp_len < 8:
                            self.wrong_mdp = True
                        else:
                            self.wrong_mdp = False
                        if not is_valid_email(self.email_input.get_text()):
                            self.wrong_email = True
                        else:
                            self.wrong_email = False
                        if pseudo_len < 3:
                            self.wrong_pseudo = True
                        else:
                            self.wrong_pseudo = False
                        if self.conf_mdp_input.get_text() != self.mdp_input.get_text() or len(
                                self.conf_mdp_input.get_text()) < 1:
                            self.wrong_conf_mdp = True
                        else:
                            self.wrong_conf_mdp = False
                        if not self.wrong_email and not self.wrong_pseudo and not self.wrong_mdp and not self.wrong_conf_mdp:
                            Log.inscription(data)
                            return

                    if self.back_button.checkinput(mouse_pos):  # retour menu
                        self.button_click_sound.play()
                        return

                    if self.connexion_txt.checkinput(mouse_pos):  # redirection inscription
                        self.button_click_sound.play()
                        return

                self.manager.process_events(event)

            self.manager.update(fps)
            self.manager.draw_ui(self.screen)
            pygame.display.update()


