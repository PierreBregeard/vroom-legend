import pygame
import pygame_gui
import sys
from ..Controler.Parties import ControlerParties
from ..Game.User import User
from ..ResourcePath import RelativePath
from .Button import Button
from ..HUD.Font import Font

clock = pygame.time.Clock()


class History:
    def __init__(self, width, height):
        self.largeur = width
        self.hauteur = height
        self.screen = pygame.display.set_mode((self.largeur, self.hauteur))
        pygame.display.set_caption("Historique")

        self.BG = pygame.image.load(RelativePath.resource_path("ressources/BackgroundMenu/Background.png"))
        self.BG = pygame.transform.scale(self.BG, (self.largeur, self.hauteur))

        self.button_click_sound = pygame.mixer.Sound(RelativePath.resource_path("ressources/Sounds/Minimalist10.mp3"))

        self.button_surface = pygame.image.load(RelativePath.resource_path("ressources/Buttons/bouton2.png"))
        self.button_surface = pygame.transform.scale(self.button_surface, (200, 100))

        self.back_button = Button(pos=(self.largeur // 8, self.hauteur * 9 / 10), text_input="Retour",
                                  font=Font.get_font(18),
                                  base_color="#d7fcd4", hovering_color="White", image=self.button_surface)

        self.run = True

        self.manager = pygame_gui.UIManager((self.largeur, self.hauteur))

        clock.tick(60)

        self.screen.blit(self.BG, (0, 0))

        self.menu_text = Font.get_font(self.largeur * 1 // 15).render("Historique", True, "#d7fcd4")
        self.menu_rect = self.menu_text.get_rect(center=(self.largeur // 2, self.hauteur * 1 // 10))

        self.data = {"pseudo": User.pseudo}
        self.allparties = ControlerParties.get_parties(self.data)

    def menu_history(self):
        while self.run:
            fps = clock.tick(60) / 1000
            mouse_pos = pygame.mouse.get_pos()

            self.screen.blit(self.BG, (0, 0))
            self.screen.blit(self.menu_text, self.menu_rect)

            for index, item in enumerate(self.allparties):
                course_text = Font.get_font(self.largeur * 1 // 70).render(f"Type de partie : {item['type']} / Temps : {format(item['time'], '.3f')}", True,
                                                                           "#FFFFFF")
                y_offset = self.hauteur * 2/10 + 30 * index
                course_rect = course_text.get_rect(center=(self.largeur * 5 / 10, y_offset))
                self.screen.blit(course_text, course_rect)

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
                    if self.back_button.checkinput(mouse_pos):
                        self.button_click_sound.play()
                        return

                self.manager.process_events(event)

            self.manager.update(fps)

            self.manager.draw_ui(self.screen)

            pygame.display.update()
