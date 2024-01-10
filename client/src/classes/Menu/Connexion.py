import sys
import pygame
import pygame_gui
import re
from .Button import Button
from .Inscription import Inscription
from src.classes.ResourcePath import RelativePath


def get_font(size):
    return pygame.font.Font(RelativePath.resource_path("ressources/Font/Pixel.ttf"), size)


def is_valid_email(email):
    email_pattern = re.compile(r'^[\w.-]+@[a-zA-Z\d.-]+\.[a-zA-Z]{2,}$')
    return bool(re.match(email_pattern, email))


clock = pygame.time.Clock()


class Connexion:
    def __init__(self, width, height):
        # à voir si on veut changer les variables en fonction de la taille de l'écran du joueur
        self.largeur, self.hauteur = width, height
        self.screen = pygame.display.set_mode((self.largeur, self.hauteur))
        pygame.display.set_caption("Connexion")

        main_font = pygame.font.SysFont("cambria", 50)
        self.BG = pygame.image.load(RelativePath.resource_path("ressources/BackgroundMenu/Background.png"))

        self.button_click_sound = pygame.mixer.Sound(RelativePath.resource_path("ressources/Sounds/Minimalist10.mp3"))

        self.BG = pygame.transform.scale(self.BG, (self.largeur, self.hauteur))

        self.manager = pygame_gui.UIManager((self.largeur, self.hauteur))

        # Redéfini la taille du bouton avec le .transform.scale
        self.button_surface = pygame.image.load(RelativePath.resource_path("ressources/Buttons/bouton2.png"))
        self.button_surface = pygame.transform.scale(self.button_surface, (200, 100))

        self.button_surface2 = pygame.image.load(RelativePath.resource_path("ressources/Buttons/bouton2red.png"))
        self.button_surface2 = pygame.transform.scale(self.button_surface2, (240, 100))

        self.menu_text = get_font(100).render("Connexion", True, "#FFFFFF")
        self.menu_rect = self.menu_text.get_rect(center=(self.largeur // 2, self.hauteur * 0.8/10))

        self.email_text = get_font(17).render("Email :", True, "#b68f40")
        self.email_rect = self.email_text.get_rect(center=(self.largeur // 7.5, self.hauteur * 2.3/10))

        self.mdp_text = get_font(17).render("Mot de passe :", True, "#b68f40")
        self.mdp_rect = self.mdp_text.get_rect(center=(self.largeur // 5, self.hauteur * 4.3/10))

        self.wrong_email_text = get_font(16).render("Veuillez entrer un email correct !", True, "#ff0000")
        self.wrong_email_rect = self.wrong_email_text.get_rect(center=(self.largeur // 2.8, self.hauteur * 3.32/10))

        self.wrong_mdp_text = get_font(16).render("Veuillez entrer votre mot de passe !", True, "#ff0000")
        self.wrong_mdp_rect = self.wrong_mdp_text.get_rect(center=(self.largeur // 2.7, self.hauteur * 5.32/10))

        self.already_co_text = get_font(16).render("Vous êtes déjà connnecté !", True, "#ff0000")
        self.already_co_rect = self.already_co_text.get_rect(center=(self.largeur // 2, self.hauteur * 7.8/10))

        self.wrong_email = False
        self.wrong_mdp = False
        self.already_co = False

        self.email_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((self.largeur // 15, self.hauteur * 2.6/10), (self.largeur // 1.7, 50)),
                                                               manager=self.manager, object_id="#pseudonyme")
        self.mdp_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((self.largeur // 15, self.hauteur * 4.6/10), (self.largeur // 1.7, 50)),
                                                             manager=self.manager, object_id="#mot_de_passe")

        self.txt_test = Button(pos=(self.largeur // 2, self.hauteur * 6.3/10), text_input="Vous n'avez pas encore de compte ? Cliquez ici !",
                               font=get_font(17),
                               base_color="#b68f40", hovering_color="White")

        self.enter_button = Button(pos=(self.largeur // 2, self.hauteur * 7/10), text_input="Connexion", font=get_font(18),
                                   base_color="#FFFFFF", hovering_color="White", image=self.button_surface2)

        self.deco_button = Button(pos=(self.largeur // 1.18, self.hauteur * 8.5/10), text_input="Déconnexion", font=get_font(18),
                                  base_color="#FFFFFF", hovering_color="White", image=self.button_surface2)

        self.back_button = Button(pos=(self.largeur // 7, self.hauteur * 8.5/10), text_input="Retour", font=get_font(18),
                                  base_color="#FFFFFF", hovering_color="White", image=self.button_surface)

        self.run = True

        self.test_deco = 1 # à enlever quand test fini

        clock.tick(60)
        pygame.display.update()

    def menu_co(self):
        while self.run:
            fps = clock.tick(60) / 1000

            mdp_len = len(self.mdp_input.get_text())

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

            # modifier le if pour vérifier si il est co, quand c'est fait, enlever les #
            # if ... :
                # self.deco_button.changecolor(mouse_pos)
                # self.deco_button.update(self.screen)

            for button in [self.enter_button, self.back_button, self.txt_test, self.deco_button]: # enlever le self.deco_button quand le if d'au dessus est fait
                button.changecolor(mouse_pos)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:  # quand l'utilisateur clique sur l'écran
                    if self.enter_button.checkinput(mouse_pos):  # Quand l'utilisateur essaye de se co via le bouton
                        self.button_click_sound.play()
                        if mdp_len < 1:
                            self.wrong_mdp = True
                        else:
                            self.wrong_mdp = False
                        if not is_valid_email(self.email_input.get_text()):
                            self.wrong_email = True
                        else:
                            self.wrong_email = False
                        if self.test_deco == 1:  # Remplacer le 1 par la requete qui vérifie si il est déjà co
                            self.already_co = True
                        else:
                            self.already_co = False
                        if not self.wrong_email and not self.wrong_mdp and not self.already_co:
                            print("Test envoi requete")  # requete à mettre ici

                    if self.back_button.checkinput(mouse_pos):  # retour menu
                        self.button_click_sound.play()
                        print("test menu")
                        return

                    if self.deco_button.checkinput(mouse_pos):  # Ajouter requete pour le deconnecter
                        self.button_click_sound.play()
                        print("Deconnexion")
                        return

                    if self.txt_test.checkinput(mouse_pos):  # redirection inscription
                        self.button_click_sound.play()
                        print("menu inscription")
                        inscr = Inscription(self.largeur, self.hauteur)
                        inscr.menu_inscr()

                self.manager.process_events(event)

            self.manager.update(fps)

            self.manager.draw_ui(self.screen)

            pygame.display.update()
