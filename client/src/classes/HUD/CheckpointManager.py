from functools import reduce

import pygame


class CheckpointManager:

    def __init__(self, screen_size):
        self.screen_size = screen_size

    def checkpoint_missed_alert(self, window):
        my_font = pygame.font.SysFont('arialblack', 20)
        text_surface = my_font.render('You missed a checkpoint, go back !', False, (0, 0, 0))
        text_size = text_surface.get_size()
        window.blit(text_surface, (self.screen_size[0]/2 - text_size[0]/2, self.screen_size[1]/2 - text_size[1]/2 - 40))

    def checkpoint_passed_HUD(self, window, checkpoint_list):
        def is_checkpoint_passed(elem):
            if elem == True:
                return True
            return False

        filtered = filter(is_checkpoint_passed, checkpoint_list)

        checkpoint_length = len(checkpoint_list)
        checkpoint_passed = reduce(lambda x, element: x + 1, filtered, 0)

        my_font = pygame.font.SysFont('arialblack', 20)
        text_surface = my_font.render(f'Checkpoints {checkpoint_passed}/{checkpoint_length}', False, (0, 0, 0))
        text_size = text_surface.get_size()
        window.blit(text_surface, (self.screen_size[0]-text_size[0], 0))