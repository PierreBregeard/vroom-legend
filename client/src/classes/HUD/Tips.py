from ..ResourcePath import RelativePath
import pygame
from .Font import Font

class Tips:

    def __init__(self, screen_size):
        self.screen_size = screen_size
        font_size = int(screen_size[0] / 50)
        self.my_font = Font.get_font(font_size)

        self.ratio = screen_size[0] / 200
        R_TIPS_path = RelativePath.resource_path("ressources/Sprites/dependencies/KEYR.png")
        self.R_TIPS = pygame.image.load(R_TIPS_path).convert_alpha()
        R_TIPS_size = self.R_TIPS.get_size()
        self.R_TIPS = pygame.transform.scale(self.R_TIPS,(int(R_TIPS_size[0] * self.ratio), int(R_TIPS_size[1] * self.ratio)))

        zqsdkey_path = RelativePath.resource_path("ressources/Sprites/dependencies/KEYSZQSD.png")
        self.zqsd_tips = pygame.image.load(zqsdkey_path).convert_alpha()
        zqsdkey_size = self.zqsd_tips.get_size()
        self.zqsd_tips = pygame.transform.scale(self.zqsd_tips,
                                             (int(zqsdkey_size[0] * self.ratio), int(zqsdkey_size[1] * self.ratio)))

    def blitTips(self, window):
        r_tips_rect = self.R_TIPS.get_rect()
        r_tips_rect.center = (
            self.ratio * 70,
            self.screen_size[1] - self.ratio * 8
        )

        zqsd_tips_rect = self.zqsd_tips.get_rect()
        zqsd_tips_rect.center = (
            self.ratio * 22,
            self.screen_size[1] - self.ratio * 14
        )

        text_surface = self.my_font.render('Last checkpoint', False, (255, 255, 255))
        text_rect = text_surface.get_rect().center = (
            self.ratio * 78,
            self.screen_size[1]-self.ratio * 8
        )

        text_surface2 = self.my_font.render('Move', False, (255, 255, 255))
        text_rect2 = text_surface2.get_rect().center = (
            self.ratio * 45,
            self.screen_size[1] - self.ratio * 8
        )
        window.blit(text_surface2, text_rect2)
        window.blit(text_surface, text_rect)
        window.blit(self.R_TIPS, r_tips_rect)
        window.blit(self.zqsd_tips, zqsd_tips_rect)
