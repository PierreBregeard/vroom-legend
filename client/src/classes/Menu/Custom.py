import sys
import pygame
import pygame_gui
from .Button import Button
from ..ResourcePath import RelativePath
from ..HUD.Font import Font


clock = pygame.time.Clock()


class Custom:
    def __init__(self, width, height):
        # à voir si on veut changer les variables en fonction de la taille de l'écran du joueur
        self.largeur, self.hauteur = width, height
        self.screen = pygame.display.set_mode((self.largeur, self.hauteur))
        pygame.display.set_caption("Customisation")

        main_font = pygame.font.SysFont("cambria", 50)
        self.BG = pygame.image.load(RelativePath.resource_path("ressources/BackgroundMenu/Background.png"))

        self.button_click_sound = pygame.mixer.Sound(RelativePath.resource_path("ressources/Sounds/Minimalist10.mp3"))

        self.BG = pygame.transform.scale(self.BG, (self.largeur, self.hauteur))

        self.menu_text = Font.get_font(70).render("Customisation", True, "#FFFFFF")
        self.menu_rect = self.menu_text.get_rect(center=(self.largeur // 2, self.hauteur * 1/10))



        self.pseudo = 1  # récup le pseudo du joueur et l'afficher dans cette variable



        self.pseudo_text = Font.get_font(20).render(f"Pseudo : {self.pseudo}", True, "#FFFFFF")
        self.pseudo_rect = self.menu_text.get_rect(center=(700, 300))  # marche pas jsp pq / s'affiche pas

        self.i = 0
        self.image_path = RelativePath.resource_path(f"ressources/sprites/test{self.i}.jpg")
        self.image = pygame.image.load(self.image_path).convert()
        self.image = pygame.transform.scale(self.image, (100, 100))

        # Redéfini la taille du bouton avec le .transform.scale
        self.button_surface = pygame.image.load(RelativePath.resource_path("ressources/Buttons/bouton2red.png"))
        self.button_surface = pygame.transform.scale(self.button_surface, (220, 90))

        self.button_surface2 = pygame.image.load(RelativePath.resource_path("ressources/Buttons/bouton2.png"))
        self.button_surface2 = pygame.transform.scale(self.button_surface2, (150, 100))

        self.next_arrow_surface = pygame.image.load(RelativePath.resource_path("ressources/Buttons/next-arrowred2.png"))
        self.next_arrow_surface = pygame.transform.scale(self.next_arrow_surface, (100, 80))

        self.prev_arrow_surface = pygame.image.load(RelativePath.resource_path("ressources/Buttons/prev-arrowred2.png"))
        self.prev_arrow_surface = pygame.transform.scale(self.prev_arrow_surface, (100, 80))

        self.manager = pygame_gui.UIManager((self.largeur, self.hauteur))

        # Changer la valeur du Font.get_font pour augmenter / diminuer la taille du text

        self.save_button = Button(pos=(self.largeur // 2, self.hauteur * 8/10), text_input="Sauvegarder", font=Font.get_font(16),
                                  base_color="#FFFFFF", hovering_color="White", image=self.button_surface)

        self.prev_button = Button(pos=(self.largeur * 1/10, self.hauteur * 6/10), text_input="", font=Font.get_font(16),
                                  base_color="#FFFFFF", hovering_color="White", image=self.prev_arrow_surface)

        self.next_button = Button(pos=(self.largeur * 9/10, self.hauteur * 6/10), text_input="", font=Font.get_font(16),
                                  base_color="#FFFFFF", hovering_color="White", image=self.next_arrow_surface)

        self.back_button = Button(pos=(self.largeur // 7, self.hauteur * 8.5/10), text_input="Retour", font=Font.get_font(16),
                                  base_color="#FFFFFF", hovering_color="White", image=self.button_surface2)

        self.run = True

        clock.tick(60)
        pygame.display.update()

    def menu_custom(self):
        while self.run:
            fps = clock.tick(60) / 1000
            mouse_pos = pygame.mouse.get_pos()

            self.screen.blit(self.BG, (0, 0))
            self.screen.blit(self.image, (self.largeur / 2, self.hauteur / 2))
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
                        self.button_click_sound.play()
                    if self.back_button.checkinput(mouse_pos):  # retour menu
                        self.button_click_sound.play()
                        return
                    if self.next_button.checkinput(mouse_pos):  # Voiture suivante
                        self.button_click_sound.play()
                        self.i = min(1, self.i + 1)
                    if self.prev_button.checkinput(mouse_pos):  # Voiture precedente
                        self.button_click_sound.play()
                        self.i = max(0, self.i - 1)

                    self.image_path = RelativePath.resource_path(f"ressources/sprites/test{self.i}.jpg")
                    self.image = pygame.image.load(self.image_path).convert()
                    self.image = pygame.transform.scale(self.image, (100, 100))

                self.manager.process_events(event)

            self.manager.update(fps)

            self.manager.draw_ui(self.screen)

            pygame.display.update()
