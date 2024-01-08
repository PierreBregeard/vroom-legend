import pygame


class Timer:

    def blit_time(self, window, time):
        my_font = pygame.font.SysFont('arialblack', 20)
        text_surface = my_font.render(str(format(time, '.3f'))+'s', False, (0, 0, 0))
        window.blit(text_surface, (20, 20))
