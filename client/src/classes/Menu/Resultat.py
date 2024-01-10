import sys
import pygame
import pygame_gui
from .Button import Button
from ..ResourcePath import RelativePath
from ..HUD.Font import Font


def get_font(size):
    return pygame.font.Font(RelativePath.resource_path("ressources/Font/Pixel.ttf"), size)


clock = pygame.time.Clock()


class Multiplayer:
    def __init__(self, width, height):
        # à voir si on veut changer les variables en fonction de la taille de l'écran du joueur
        self.largeur, self.hauteur = width, height
        self.screen = pygame.display.set_mode((self.largeur, self.hauteur))
        pygame.display.set_caption("Résultat")

        main_font = pygame.font.SysFont("cambria", 50)
        self.BG = pygame.image.load(RelativePath.resource_path("ressources/BackgroundMenu/Background.png"))

        self.button_click_sound = pygame.mixer.Sound(RelativePath.resource_path("ressources/Sounds/Minimalist10.mp3"))

        self.BG = pygame.transform.scale(self.BG, (self.largeur, self.hauteur))

        self.menu_text = get_font(100).render("Résultat", True, "#FFFFFF")
        self.menu_rect = self.menu_text.get_rect(center=(750, 100))

        # Redéfini la taille du bouton avec le .transform.scale
        self.button_surface = pygame.image.load(RelativePath.resource_path("ressources/Buttons/bouton2red.png"))
        self.button_surface = pygame.transform.scale(self.button_surface, (220, 90))

        self.button_surface2 = pygame.image.load(RelativePath.resource_path("ressources/Buttons/bouton2.png"))
        self.button_surface2 = pygame.transform.scale(self.button_surface2, (150, 100))

        self.manager = pygame_gui.UIManager((self.largeur, self.hauteur))

        self.back_button = Button(pos=(125, 800), text_input="Retour", font=get_font(16),
                                  base_color="#FFFFFF", hovering_color="White", image=self.button_surface2)

        self.run = True

        clock.tick(60)
        pygame.display.update()

    def menu_multi(self):
        while self.run:
            fps = clock.tick(60) / 1000
            mouse_pos = pygame.mouse.get_pos()

            self.screen.blit(self.BG, (0, 0))
            self.screen.blit(self.menu_text, self.menu_rect)

            for button in [self.back_button]:
                button.changecolor(mouse_pos)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.checkinput(mouse_pos):  # retour menu
                        self.button_click_sound.play()
                        return

                self.manager.process_events(event)

            self.manager.update(fps)

            self.manager.draw_ui(self.screen)

            pygame.display.update()
