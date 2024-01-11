import sys
import pygame
import pygame_gui
from .Button import Button
from ..ResourcePath import RelativePath
from ..HUD.Font import Font

clock = pygame.time.Clock()


class WaitingRoom:
    def __init__(self, width, height):
        # à voir si on veut changer les variables en fonction de la taille de l'écran du joueur
        self.largeur, self.hauteur = width, height
        self.screen = pygame.display.set_mode((self.largeur, self.hauteur))
        pygame.display.set_caption("Waiting Room")

        main_font = pygame.font.SysFont("cambria", 50)
        self.BG = pygame.image.load(RelativePath.resource_path("ressources/BackgroundMenu/Background.png"))

        self.button_click_sound = pygame.mixer.Sound(RelativePath.resource_path("ressources/Sounds/Minimalist10.mp3"))

        self.BG = pygame.transform.scale(self.BG, (self.largeur, self.hauteur))

        self.menu_text = Font.get_font(self.largeur * 1 // 15).render("Waiting Room", True, "#FFFFFF")
        self.menu_rect = self.menu_text.get_rect(center=(self.largeur // 2, self.hauteur * 1 / 10))

        self.list_text = Font.get_font(self.largeur * 1 // 70).render("Joueurs :", True, "#FFFFFF")
        self.list_rect = self.list_text.get_rect(center=(self.largeur * 2 / 10, self.hauteur * 2 / 10))

        # Redéfini la taille du bouton avec le .transform.scale
        self.button_surface = pygame.image.load(RelativePath.resource_path("ressources/Buttons/bouton2red.png"))
        self.button_surface = pygame.transform.scale(self.button_surface, (220, 90))

        self.button_surface2 = pygame.image.load(RelativePath.resource_path("ressources/Buttons/bouton2.png"))
        self.button_surface2 = pygame.transform.scale(self.button_surface2, (150, 100))

        self.manager = pygame_gui.UIManager((self.largeur, self.hauteur))

        self.back_button = Button(pos=(self.largeur // 8, self.hauteur * 9 / 10), text_input="Retour",
                                  font=Font.get_font(16),
                                  base_color="#FFFFFF", hovering_color="White", image=self.button_surface2)

        self.start_button = Button(pos=(self.largeur // 8, self.hauteur * 9 / 10), text_input="Start",
                                   font=Font.get_font(16),
                                   base_color="#FFFFFF", hovering_color="White", image=self.button_surface)

        self.run = True

        clock.tick(60)
        pygame.display.update()

    def menu_wait(self, role):
        while self.run:
            fps = clock.tick(60) / 1000
            mouse_pos = pygame.mouse.get_pos()

            self.screen.blit(self.BG, (0, 0))
            self.screen.blit(self.menu_text, self.menu_rect)
            self.screen.blit(self.list_text, self.list_rect)

            # if ... :
            # self.start_button.changecolor(mouse_pos)
            # self.start_button.update(self.screen)

            for button in [self.back_button]:
                button.changecolor(mouse_pos)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button != 1:
                        continue
                    if self.back_button.checkinput(mouse_pos):  # retour menu
                        self.button_click_sound.play()
                        # le faire déco de la salle / fermer la salle et return un message d'erreur au menu principal
                        return

                self.manager.process_events(event)

            self.manager.update(fps)

            self.manager.draw_ui(self.screen)

            pygame.display.update()
