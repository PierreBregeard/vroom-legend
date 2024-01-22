from .Effect import Effect
import pygame


class TireEffect(Effect):
    def __init__(self, pos, angle, duration):
        super().__init__(duration)
        self.image = pygame.surface.Surface((2, 5))
        self.image.fill((0, 0, 0))
        self.image = pygame.transform.rotozoom(self.image, angle, 1)
        self.rect = self.image.get_rect(center=pos)
