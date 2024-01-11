import pygame
from .Font import Font


class Timer:

    time = 0

    def __init__(self):
        self.my_font = Font.get_font(20)

    def blit_time(self, window):
        text_surface = self.my_font.render(str(format(self.time, '.3f')) + 's', False, (0, 0, 0))
        window.blit(text_surface, (20, 20))
