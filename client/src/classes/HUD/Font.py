import pygame
from ..ResourcePath import RelativePath


class Font:

    @staticmethod
    def get_font(size):
        return pygame.font.Font(RelativePath.resource_path("ressources/Font/Pixel.ttf"), size)
