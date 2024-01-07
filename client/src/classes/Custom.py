import os
import sys
import pygame
import pygame_gui
from src.classes.button import Button

os.chdir(os.path.dirname(__file__))


# from src.main import init_menu
# from src.classes.Inscription import Inscription


def get_font(size):
    return pygame.font.Font("../ressources/Font/Roboto-Black.ttf", size)


clock = pygame.time.Clock()


class Custom:
    def __init__(self):
        pygame.init()
        # à voir si on veut changer les variables en fonction de la taille de l'écran du joueur
        self.largeur, self.hauteur = 1000, 720
        self.screen = pygame.display.set_mode((self.largeur, self.hauteur))
        pygame.display.set_caption("Customisation")
        self.screen.fill("black")

        self.i = 0
        self.image_path = f"../ressources/sprites/test{self.i}.jpg"
        self.image = pygame.image.load(self.image_path).convert()
        self.image = pygame.transform.scale(self.image, (100, 100))

        self.menu_text = get_font(100).render("Vroom Legends", True, "#b68f40")
        self.menu_rect = self.menu_text.get_rect(center=(500, 90))



        self.pseudo = 1  # récup le pseudo du joueur et l'afficher dans cette variable



        self.pseudo_text = get_font(20).render(f"Pseudo : {self.pseudo}", True, "#FFFFFF")
        self.pseudo_rect = self.menu_text.get_rect(center=(400, 230))

        main_font = pygame.font.SysFont("cambria", 50)
        self.BG = pygame.image.load("../ressources/BackgroundMenu/Background.png")

        # Redéfini la taille du bouton avec le .transform.scale
        self.button_surface = pygame.image.load("../ressources/Buttons/bouton1.png")
        self.button_surface = pygame.transform.scale(self.button_surface, (150, 100))

        self.manager = pygame_gui.UIManager((self.largeur, self.hauteur))

        # Changer la valeur du get_font pour augmenter / diminuer la taille du text

        self.save_button = Button(pos=(500, 600), text_input="Sauvegarder", font=get_font(22),
                                  base_color="#d7fcd4", hovering_color="White", image=self.button_surface)

        self.prev_button = Button(pos=(100, 450), text_input="Precedent", font=get_font(25),
                                  base_color="#d7fcd4", hovering_color="White", image=self.button_surface)

        self.next_button = Button(pos=(900, 450), text_input="Suivant", font=get_font(25),
                                  base_color="#d7fcd4", hovering_color="White", image=self.button_surface)

        self.back_button = Button(pos=(150, 600), text_input="Retour", font=get_font(35),
                                  base_color="#d7fcd4", hovering_color="White", image=self.button_surface)

        self.run = True

        clock.tick(60)
        pygame.display.update()

    def menu_custom(self):
        while self.run:
            fps = clock.tick(60) / 1000
            mouse_pos = pygame.mouse.get_pos()

            self.screen.blit(self.BG, (0, 0))
            self.screen.blit(self.image, (450, 300))
            self.screen.blit(self.menu_text, self.menu_rect)
            self.screen.blit(self.pseudo_text, self.pseudo_rect)

            for button in [self.save_button, self.back_button, self.prev_button, self.next_button]:
                button.changecolor(mouse_pos)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.save_button.checkinput(mouse_pos):  # rajouter les requetes pour la sauvegarde
                        print("test save click")
                    if self.back_button.checkinput(mouse_pos):  # retour menu
                        print("test menu")
                        # init_menu()
                    if self.next_button.checkinput(mouse_pos):  # Voiture suivante
                        self.i = min(1, self.i + 1)
                    if self.prev_button.checkinput(mouse_pos):  # Voiture precedente
                        self.i = max(0, self.i - 1)

                    self.image_path = f"../ressources/sprites/test{self.i}.jpg"
                    self.image = pygame.image.load(self.image_path).convert()
                    self.image = pygame.transform.scale(self.image, (100, 100))

                self.manager.process_events(event)

            self.manager.update(fps)

            self.manager.draw_ui(self.screen)

            pygame.display.update()


test = Custom()
test.menu_custom()
