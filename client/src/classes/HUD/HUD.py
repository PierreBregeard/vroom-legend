import pygame

from .Speedometer import Speedometer
from .CheckpointManager import CheckpointManager


class HUD:

    def __init__(self, screen_size, max_speed):
        self.has_missed_checkpoint = False
        self.speedometer = Speedometer(screen_size, max_speed)
        self.checkpoint_manager = CheckpointManager(screen_size)

    def blit_HUD(self, window, checkpoint_list):
        self.speedometer.blit_speedometer(window)
        self.checkpoint_manager.checkpoint_passed_HUD(window, checkpoint_list)
        if self.has_missed_checkpoint:
            self.checkpoint_manager.checkpoint_missed_alert(window)
