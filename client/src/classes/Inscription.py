import sys
import pygame
import pygame_gui
import re
from src.classes.button import Button


# from src.main import init_menu
# from src.classes.Inscription import Inscription


def get_font(size):
    return pygame.font.Font("../ressources/Font/Roboto-Black.ttf", size)


def is_valid_email(email):
    email_pattern = re.compile(r'^[\w.-]+@[a-zA-Z\d.-]+\.[a-zA-Z]{2,}$')
    return bool(re.match(email_pattern, email))


clock = pygame.time.Clock()


class Inscription:
    def __init__(self):
        pygame.init()
        # à voir si on veut changer les variables en fonction de la taille de l'écran du joueur
        self.largeur, self.hauteur = 1500, 900
        self.screen = pygame.display.set_mode((self.largeur, self.hauteur))
        pygame.display.set_caption("Inscription")
        self.screen.fill("black")

        self.menu_text = get_font(100).render("Vroom Legends", True, "#b68f40")
        self.menu_rect = self.menu_text.get_rect(center=(700, 90))

        self.pseudo_text = get_font(17).render("Pseudo :", True, "#b68f40")
        self.pseudo_rect = self.menu_text.get_rect(center=(860, 230))

        self.email_text = get_font(17).render("Email :", True, "#b68f40")
        self.email_rect = self.menu_text.get_rect(center=(860, 360))

        self.mdp_text = get_font(17).render("Mot de passe :", True, "#b68f40")
        self.mdp_rect = self.menu_text.get_rect(center=(860, 490))

        self.conf_mdp_text = get_font(17).render("Confirmez :", True, "#b68f40")
        self.conf_mdp_rect = self.menu_text.get_rect(center=(860, 620))

        self.wrong_pseudo_text = get_font(17).render("Veuillez entrer un pseudo de plus de 3 caractères !", True,"#ff0000")
        self.wrong_pseudo_rect = self.menu_text.get_rect(center=(860, 320))

        self.wrong_email_text = get_font(17).render("Veuillez entrer un email correct !", True, "#ff0000")
        self.wrong_email_rect = self.menu_text.get_rect(center=(860, 450))

        self.wrong_mdp_text = get_font(17).render("Votre mot de passe doit faire au moins 8 caractères !", True,"#ff0000")
        self.wrong_mdp_rect = self.menu_text.get_rect(center=(860, 580))

        self.wrong_conf_mdp_text = get_font(17).render("Vos mots de passes doivent être identiques !", True, "#ff0000")
        self.wrong_conf_mdp_rect = self.menu_text.get_rect(center=(860, 710))

        self.wrong_email = False
        self.wrong_pseudo = False
        self.wrong_mdp = False
        self.wrong_conf_mdp = False

        main_font = pygame.font.SysFont("cambria", 50)
        self.BG = pygame.image.load("../ressources/BackgroundMenu/Background.png")

        self.BG = pygame.transform.scale(self.BG, (self.largeur, self.hauteur))

        self.button_click_sound = pygame.mixer.Sound("../ressources/Sounds/Minimalist10.mp3")

        # Redéfini la taille du bouton avec le .transform.scale
        self.button_surface = pygame.image.load("../ressources/Buttons/bouton1.png")
        self.button_surface = pygame.transform.scale(self.button_surface, (150, 100))

        self.manager = pygame_gui.UIManager((self.largeur, self.hauteur))

        self.pseudo_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((500, 200), (400, 50)),
                                                               manager=self.manager, object_id="#pseudonyme")
        self.email_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((500, 330), (400, 50)),
                                                                manager=self.manager, object_id="#email")
        self.mdp_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((500, 460), (400, 50)),
                                                             manager=self.manager, object_id="#mot_de_passe")
        self.conf_mdp_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((500, 590), (400, 50)),
                                                                  manager=self.manager, object_id="#conf_mot_de_passe")

        self.connexion_txt = Button(pos=(700, 750), text_input="Vous avez déjà un compte ? Cliquez ici !",
                                    font=get_font(17),
                                    base_color="#d7fcd4", hovering_color="White")

        self.enter_button = Button(pos=(700, 820), text_input="S'inscrire", font=get_font(25),
                                   base_color="#d7fcd4", hovering_color="White", image=self.button_surface)

        self.back_button = Button(pos=(150, 800), text_input="Retour", font=get_font(35),
                                  base_color="#d7fcd4", hovering_color="White", image=self.button_surface)

        self.run = True

        clock.tick(60)
        pygame.display.update()

    def menu_inscr(self):
        while self.run:
            fps = clock.tick(60) / 1000

            pseudo_len = len(self.pseudo_input.get_text())
            mdp_len = len(self.mdp_input.get_text())
            conf_mdp_len = len(self.conf_mdp_input.get_text())

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

            for button in [self.enter_button, self.back_button, self.connexion_txt]: # pas toucher
                button.changecolor(mouse_pos)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN: # quand tu clique sur l'écran
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
                        if self.conf_mdp_input.get_text() != self.mdp_input.get_text() or len(self.conf_mdp_input.get_text()) < 1:
                            self.wrong_conf_mdp = True
                        else:
                            self.wrong_conf_mdp = False
                        if not self.wrong_email and not self.wrong_pseudo and not self.wrong_mdp and not self.wrong_conf_mdp:
                            print("Test envoi requete")  # requete à mettre ici

                    if self.back_button.checkinput(mouse_pos):  # retour menu
                        self.button_click_sound.play()
                        print("menu principal")
                        # init_menu()

                    if self.connexion_txt.checkinput(mouse_pos):  # redirection inscription
                        self.button_click_sound.play()
                        print("menu connexion")
                        # init_connexion()

                self.manager.process_events(event)

            self.manager.update(fps)
            self.manager.draw_ui(self.screen)
            pygame.display.update()


test = Inscription()
test.menu_inscr()
