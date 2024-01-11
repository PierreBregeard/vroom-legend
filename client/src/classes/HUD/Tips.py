from ..ResourcePath import RelativePath
import pygame
from .Font import Font

class Tips:

    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.my_font = Font.get_font(20)
        R_TIPS_path = RelativePath.resource_path("ressources/sprites/dependencies/KEYR.png")
        self.R_TIPS = pygame.image.load(R_TIPS_path).convert_alpha()
        R_TIPS_size = self.R_TIPS.get_size()
        self.ratio = 8
        self.R_TIPS = pygame.transform.scale(
            self.R_TIPS,
            (int(R_TIPS_size[0] * self.ratio), int(R_TIPS_size[1] * self.ratio))
        )

    def blitTips(self, window):
        r_tips_rect = self.R_TIPS.get_rect()
        r_tips_rect.center = (
            self.ratio * 8,
            self.screen_size[1]-self.ratio * 8
        )
        text_surface = self.my_font.render('Last checkpoint', False, (0, 0, 0))
        text_rect = text_surface.get_rect().center = (
            self.ratio * 8 + self.ratio * 10,
            self.screen_size[1]-self.ratio * 8
        )
        window.blit(text_surface, text_rect)
        window.blit(self.R_TIPS, r_tips_rect)
