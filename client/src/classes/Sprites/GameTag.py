import pygame.sprite
from ..HUD.Font import Font


class GameTag(pygame.sprite.Sprite):

    def __init__(self, pseudo, pos):
        super().__init__()
        self.image = Font.get_font(10).render(pseudo, True, (255, 255, 255)).fill((0, 0, 0, .5))
        self.rect.center = pos
