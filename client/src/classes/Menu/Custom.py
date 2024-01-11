import sys
import pygame
import pygame_gui
from .Button import Button
from ..Controler.Color import ControllerColor
from ..Game.User import User
from ..ResourcePath import RelativePath
from ..HUD.Font import Font


clock = pygame.time.Clock()


def create_hsv_surface(width, height):
    hsv_surf = pygame.Surface((width, height))
    for x in range(width):
        for y in range(height):
            hue = x / width * 360
            sat = y / height
            value = 1
            color = pygame.Color(0)
            color.hsva = (hue, sat * 100, value * 80, 100)
            hsv_surf.set_at((x, y), color)
    return hsv_surf


class Custom:
    def __init__(self, width, height):
        self.largeur, self.hauteur = width, height
        self.screen = pygame.display.set_mode((self.largeur, self.hauteur))
        pygame.display.set_caption("Customisation")

        self.BG = pygame.image.load(RelativePath.resource_path("ressources/BackgroundMenu/Background.png"))

        self.button_click_sound = pygame.mixer.Sound(RelativePath.resource_path("ressources/Sounds/Minimalist10.mp3"))

        self.BG = pygame.transform.scale(self.BG, (self.largeur, self.hauteur))

        self.menu_text = Font.get_font(self.largeur * 1//15).render("Customisation", True, "#FFFFFF")
        self.menu_rect = self.menu_text.get_rect(center=(self.largeur * 5/10, self.hauteur * 1 / 10))

        self.button_surface = pygame.image.load(RelativePath.resource_path("ressources/Buttons/bouton2red.png"))
        self.button_surface = pygame.transform.scale(self.button_surface, (self.largeur * 2/9, self.hauteur * 1/11))

        self.button_surface2 = pygame.image.load(RelativePath.resource_path("ressources/Buttons/bouton2.png"))
        self.button_surface2 = pygame.transform.scale(self.button_surface2, (self.largeur * 1/5, self.hauteur * 1/10))

        self.manager = pygame_gui.UIManager((self.largeur, self.hauteur))

        self.save_button = Button(pos=(self.largeur // 2, self.hauteur * 7 / 10), text_input="Sauvegarder",
                                  font=Font.get_font(16),
                                  base_color="#FFFFFF", hovering_color="White", image=self.button_surface)

        self.roof_button = Button(pos=(self.largeur * 1 / 10, self.hauteur * 5 / 10), text_input="Toit",
                                  font=Font.get_font(16),
                                  base_color="#FFFFFF", hovering_color="White", image=self.button_surface2)

        self.car_button = Button(pos=(self.largeur * 9 / 10, self.hauteur * 5 / 10), text_input="Caisse",
                                 font=Font.get_font(16),
                                 base_color="#FFFFFF", hovering_color="White", image=self.button_surface2)

        self.back_button = Button(pos=(self.largeur * 1 / 10, self.hauteur * 9 / 10), text_input="Retour",
                                  font=Font.get_font(16),
                                  base_color="#FFFFFF", hovering_color="White", image=self.button_surface2)

        self.hsv_picker = create_hsv_surface(360, 100)
        self.hsv_picker_rect = self.hsv_picker.get_rect(center=(self.largeur * 5 / 10, self.hauteur * 5 / 10))

        self.selected_color2 = User.color2  # toit
        self.color2_rect = (self.largeur * 2 / 10, self.hauteur * 10 / 17, 50, 50)
        self.selected_color1 = User.color1  # caisse
        self.color1_rect = (self.largeur * 9 / 12, self.hauteur * 10 / 17, 50, 50)

        self.current_color = 1  # 1 or 2

        self.run = True

        clock.tick(60)
        pygame.display.update()

    def menu_custom(self):
        while self.run:
            fps = clock.tick(60) / 1000
            mouse_pos = pygame.mouse.get_pos()

            self.screen.blit(self.BG, (0, 0))
            self.screen.blit(self.menu_text, self.menu_rect)
            self.screen.blit(self.hsv_picker, self.hsv_picker_rect)
            pygame.draw.rect(self.screen, self.selected_color1, self.color1_rect)
            pygame.draw.rect(self.screen, self.selected_color2, self.color2_rect)

            color1 = [self.selected_color2[0], self.selected_color2[1], self.selected_color2[2]]
            color2 = [self.selected_color1[0], self.selected_color1[1], self.selected_color1[2]]
            data = {"pseudo": User.pseudo, "car": {"color1": color1, "color2": color2}}

            for button in [self.save_button, self.back_button, self.car_button, self.roof_button]:
                button.changecolor(mouse_pos)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.save_button.checkinput(mouse_pos):
                        self.button_click_sound.play()
                        if len(User.pseudo) > 1:
                            ControllerColor.change_color(data)
                            return
                        else:
                            User.color1 = color1
                            User.color2 = color2
                            print(User.color1)
                            print(User.color2)
                            return

                    if self.back_button.checkinput(mouse_pos):  # retour menu
                        self.button_click_sound.play()
                        return

                    if self.car_button.checkinput(mouse_pos):
                        self.button_click_sound.play()
                        self.current_color = "Caisse"

                    if self.roof_button.checkinput(mouse_pos):
                        self.button_click_sound.play()
                        self.current_color = "Toit"

                    if self.hsv_picker_rect.collidepoint(event.pos):
                        self.button_click_sound.play()
                        x, y = event.pos[0] - self.hsv_picker_rect.x, event.pos[1] - self.hsv_picker_rect.y
                        selected_color = self.hsv_picker.get_at((x, y))
                        if self.current_color == "Caisse":
                            self.selected_color1 = selected_color
                        else:
                            self.selected_color2 = selected_color

                self.manager.process_events(event)

            self.manager.update(fps)

            self.manager.draw_ui(self.screen)

            pygame.display.update()
