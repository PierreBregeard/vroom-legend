import sys
import pygame
import pygame_gui
from src.classes.button import Button
# from src.main import init_menu
# from src.classes.Inscription import Inscription


def get_font(size):
    return pygame.font.Font("../ressources/Font/Roboto-Black.ttf", size)


clock = pygame.time.Clock()


class Connexion:
    def __init__(self):
        pygame.init()
        # à voir si on veut changer les variables en fonction de la taille de l'écran du joueur
        self.largeur, self.hauteur = 1000, 720
        self.screen = pygame.display.set_mode((self.largeur, self.hauteur))
        pygame.display.set_caption("Connexion")
        self.screen.fill("black")

        self.menu_text = get_font(100).render("Vroom Legends", True, "#b68f40")
        self.menu_rect = self.menu_text.get_rect(center=(500, 90))

        self.pseudo_text = get_font(17).render("Pseudo :", True, "#b68f40")
        self.pseudo_rect = self.menu_text.get_rect(center=(665, 230))

        self.mdp_text = get_font(17).render("Mot de passe :", True, "#b68f40")
        self.mdp_rect = self.menu_text.get_rect(center=(665, 330))

        main_font = pygame.font.SysFont("cambria", 50)
        self.BG = pygame.image.load("../ressources/BackgroundMenu/Background.png")

        # Redéfini la taille du bouton avec le .transform.scale
        self.button_surface = pygame.image.load("../ressources/Buttons/bouton1.png")
        self.button_surface = pygame.transform.scale(self.button_surface, (150, 100))

        self.manager = pygame_gui.UIManager((self.largeur, self.hauteur))

        self.pseudo_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((300, 200), (400, 50)),
                                                                manager=self.manager, object_id="#pseudonyme")
        self.mdp_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((300, 300), (400, 50)),
                                                             manager=self.manager, object_id="#mot_de_passe")

        self.txt_test = Button(pos=(500, 380), text_input="Vous n'avez pas encore de compte ? Cliquez ici !", font=get_font(17),
                               base_color="#d7fcd4", hovering_color="White")

        self.enter_button = Button(pos=(500, 450), text_input="Connexion", font=get_font(25),
                                   base_color="#d7fcd4", hovering_color="White", image=self.button_surface)

        self.back_button = Button(pos=(150, 600), text_input="Retour", font=get_font(35),
                                  base_color="#d7fcd4", hovering_color="White", image=self.button_surface)

        self.run = True

        clock.tick(60)
        pygame.display.update()

    def menu_co(self):
        while self.run:
            fps = clock.tick(60) / 1000

            test_mdp = len(self.mdp_input.get_text())

            self.screen.blit(self.BG, (0, 0))

            mouse_pos = pygame.mouse.get_pos()

            self.screen.blit(self.menu_text, self.menu_rect)
            self.screen.blit(self.pseudo_text, self.pseudo_rect)
            self.screen.blit(self.mdp_text, self.mdp_rect)

            for button in [self.enter_button, self.back_button, self.txt_test]:
                button.changecolor(mouse_pos)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:  # rajouter les requetes pour la connexion
                    print("Test touche entrée")
                if self.enter_button.checkinput(mouse_pos) and test_mdp > 3:  # test pour voir si ça marche
                    print("test entrée click")
                if self.back_button.checkinput(mouse_pos):  # retour menu
                    print("test menu")
                    # init_menu()
                if self.txt_test.checkinput(mouse_pos): # redirection inscription
                    print("menu inscription")
                    # init_inscription()

                self.manager.process_events(event)

            self.manager.update(fps)

            self.manager.draw_ui(self.screen)

            pygame.display.update()


test = Connexion()
test.menu_co()

