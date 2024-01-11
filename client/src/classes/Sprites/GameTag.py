import pygame.sprite
from ..HUD.Font import Font


class GameTag(pygame.sprite.Sprite):

    space_between = 40

    def __init__(self, pseudo, pos):
        super().__init__()
        font_img = Font.get_font(15).render(pseudo, True, (255, 255, 255))
        self.image = font_img.copy()
        self.image.fill((0, 0, 0, 50))
        self.image.blit(font_img, (0, 0))
        self.rect = self.image.get_rect(center=(pos[0], pos[1] - self.space_between))

    def change_pos(self, pos):
        self.rect.center = (pos[0], pos[1] - self.space_between)

    def update(self):
        super().update()
