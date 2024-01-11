from functools import reduce

import pygame
from .Font import Font

class CheckpointManager:

    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.my_font = Font.get_font(20)
        self.checkpoint_list = []
        size = int(screen_size[0] / 50)
        self.my_font = Font.get_font(size)

    def checkpoint_missed_alert(self, window):

        text_surface = self.my_font.render('You missed a checkpoint, go back !', False, (255, 255, 255))
        text_size = text_surface.get_size()
        window.blit(text_surface, (self.screen_size[0]/2 - text_size[0]/2, self.screen_size[1]/2 - text_size[1]/2 - 40))

    def checkpoint_passed_HUD(self, window):
        def is_checkpoint_passed(elem):
            return bool(elem)

        filtered = filter(is_checkpoint_passed, self.checkpoint_list)

        checkpoint_length = len(self.checkpoint_list)
        checkpoint_passed = reduce(lambda x, element: x + 1, filtered, 0)

        text_surface = self.my_font.render(f'Checkpoints {checkpoint_passed}/{checkpoint_length}', False, (255, 255, 255))
        text_size = text_surface.get_size()
        window.blit(text_surface, (self.screen_size[0]-text_size[0]-20, 20))

    def no_last_checkpoint(self, window):
        text_surface = self.my_font.render("You haven't passed any checkpoint yet", False, (255, 255, 255))
        text_size = text_surface.get_size()
        window.blit(text_surface,
                    (self.screen_size[0] / 2 - text_size[0] / 2, self.screen_size[1] / 2 - text_size[1] / 2 - 40))
