import pygame

from .Speedometer import Speedometer
from .CheckpointManager import CheckpointManager
from .Timer import Timer


class HUD:

    def __init__(self, screen_size, max_speed):
        self.has_missed_checkpoint = False
        self.speedometer = Speedometer(screen_size, max_speed)
        self.checkpoint_manager = CheckpointManager(screen_size)
        self.timer = Timer()


    def blit_HUD(self, window, checkpoint_list, current_time):
        self.speedometer.blit_speedometer(window)
        self.checkpoint_manager.checkpoint_passed_HUD(window, checkpoint_list)
        self.timer.blit_time(window, current_time)
        if self.has_missed_checkpoint:
            self.checkpoint_manager.checkpoint_missed_alert(window)
