import pygame
from .Font import Font


class Timer:
    def __init__(self, window_size):
        size = int(window_size[0]/50)
        self.my_font = Font.get_font(size)

    def blit_time(self, window, time):
        text_surface = self.my_font.render(str(format(time, '.3f')) + 's', False, (255, 255, 255))
        window.blit(text_surface, (20, 20))
