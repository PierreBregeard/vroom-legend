import sys
import pygame
import pygame_gui
import re
from .Button import Button
from .Inscription import Inscription
from ..Controler.Color import ControllerColor
from ..Game.User import User
from ..ResourcePath import RelativePath
from ..HUD.Font import Font


def is_valid_email(email):
    email_pattern = re.compile(r'^[\w.-]+@[a-zA-Z\d.-]+\.[a-zA-Z]{2,}$')
    return bool(re.match(email_pattern, email))


clock = pygame.time.Clock()


class Connexion:
    def __init__(self, width, height):
        self.largeur, self.hauteur = width, height
        self.screen = pygame.display.set_mode((self.largeur, self.hauteur))
        pygame.display.set_caption("Connexion")

        self.BG = pygame.image.load(RelativePath.resource_path("ressources/BackgroundMenu/Background.png"))

        self.button_click_sound = pygame.mixer.Sound(RelativePath.resource_path("ressources/Sounds/Minimalist10.mp3"))

        self.BG = pygame.transform.scale(self.BG, (self.largeur, self.hauteur))

        self.manager = pygame_gui.UIManager((self.largeur, self.hauteur))

        self.button_surface = pygame.image.load(RelativePath.resource_path("ressources/Buttons/bouton2.png"))
        self.button_surface = pygame.transform.scale(self.button_surface, (self.largeur * 1/5, self.hauteur * 1/10))

        self.button_surface2 = pygame.image.load(RelativePath.resource_path("ressources/Buttons/bouton2red.png"))
        self.button_surface2 = pygame.transform.scale(self.button_surface2, (self.largeur * 2/9, self.hauteur * 1/11))

        self.menu_text = Font.get_font(self.largeur * 1 // 15).render("Connexion", True, "#FFFFFF")
        self.menu_rect = self.menu_text.get_rect(center=(self.largeur * 5/10, self.hauteur * 1 / 10))

        self.email_text = Font.get_font(self.largeur * 1//55).render("Email :", True, "#b68f40")
        self.email_rect = self.email_text.get_rect(center=(self.largeur * 2/15, self.hauteur * 5 / 23))

        self.mdp_text = Font.get_font(self.largeur * 1//55).render("Mot de passe :", True, "#b68f40")
        self.mdp_rect = self.mdp_text.get_rect(center=(self.largeur * 2/10, self.hauteur * 7/16))

        self.wrong_email_text = Font.get_font(self.largeur * 1//55).render("Veuillez entrer un email correct !", True, "#ff0000")
        self.wrong_email_rect = self.wrong_email_text.get_rect(center=(self.largeur * 7/19, self.hauteur * 10 / 30))

        self.wrong_mdp_text = Font.get_font(self.largeur * 1//55).render("Veuillez entrer votre mot de passe !", True, "#ff0000")
        self.wrong_mdp_rect = self.wrong_mdp_text.get_rect(center=(self.largeur * 7/18, self.hauteur * 16 / 30))

        self.already_co_text = Font.get_font(self.largeur * 1//55).render("Vous êtes déjà connnecté !", True, "#ff0000")
        self.already_co_rect = self.already_co_text.get_rect(center=(self.largeur * 5/10, self.hauteur * 10 / 13))

        self.wrong_email = False
        self.wrong_mdp = False
        self.already_co = False

        self.email_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((self.largeur // 15, self.hauteur * 3 / 12), (self.largeur * 9/15, 50)),
            manager=self.manager, object_id="#pseudonyme")
        self.mdp_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((self.largeur // 15, self.hauteur * 5/11), (self.largeur * 9/15, 50)),
            manager=self.manager, object_id="#mot_de_passe")

        self.mdp_input.set_text_hidden(True)

        self.txt_test = Button(pos=(self.largeur // 2, self.hauteur * 7 / 10),
                               text_input="Vous n'avez pas encore de compte ? Cliquez ici !",
                               font=Font.get_font(self.largeur * 1//55),
                               base_color="#b68f40", hovering_color="White")

        self.enter_button = Button(pos=(self.largeur * 5/10, self.hauteur * 10 / 16), text_input="Connexion",
                                   font=Font.get_font(self.largeur * 1//55),
                                   base_color="#FFFFFF", hovering_color="White", image=self.button_surface2)

        self.back_button = Button(pos=(self.largeur * 2/13, self.hauteur * 11 / 13), text_input="Retour",
                                  font=Font.get_font(self.largeur * 1//55),
                                  base_color="#FFFFFF", hovering_color="White", image=self.button_surface)

        self.run = True

        self.test_deco = 1  # à enlever quand test fini

        clock.tick(60)
        pygame.display.update()

    def menu_co(self):
        while self.run:
            fps = clock.tick(60) / 1000

            mdp_len = len(self.mdp_input.get_text())
            data = {"email": self.email_input.get_text(), "mdp": self.mdp_input.get_text()}

            self.screen.blit(self.BG, (0, 0))

            mouse_pos = pygame.mouse.get_pos()

            self.screen.blit(self.menu_text, self.menu_rect)
            self.screen.blit(self.email_text, self.email_rect)
            self.screen.blit(self.mdp_text, self.mdp_rect)

            if self.wrong_email:
                self.screen.blit(self.wrong_email_text, self.wrong_email_rect)
            if self.wrong_mdp:
                self.screen.blit(self.wrong_mdp_text, self.wrong_mdp_rect)
            if self.already_co:
                self.screen.blit(self.already_co_text, self.already_co_rect)

            for button in [self.enter_button, self.back_button, self.txt_test]:
                button.changecolor(mouse_pos)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button != 1:
                        continue
                    if self.enter_button.checkinput(mouse_pos):
                        self.button_click_sound.play()
                        if mdp_len < 1:
                            self.wrong_mdp = True
                        else:
                            self.wrong_mdp = False
                        if not is_valid_email(self.email_input.get_text()):
                            self.wrong_email = True
                        else:
                            self.wrong_email = False
                        if len(User.pseudo) > 1:
                            self.already_co = True
                        else:
                            self.already_co = False
                        if not self.wrong_email and not self.wrong_mdp and not self.already_co:
                            User.connexion(data)
                            datapseudo = {"pseudo": User.pseudo}
                            color = ControllerColor.get_color(datapseudo)
                            color1 = color['color1']
                            color2 = color['color2']
                            User.color1 = color1
                            User.color2 = color2
                            return

                    if self.back_button.checkinput(mouse_pos):  # retour menu
                        self.button_click_sound.play()
                        return

                    if self.txt_test.checkinput(mouse_pos):
                        self.button_click_sound.play()
                        inscr = Inscription(self.largeur, self.hauteur)
                        inscr.menu_inscr()

                self.manager.process_events(event)

            self.manager.update(fps)

            self.manager.draw_ui(self.screen)

            pygame.display.update()
