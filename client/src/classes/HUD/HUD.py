from .Speedometer import Speedometer


class HUD:

    def __init__(self, screen_size):
        self.speedometer = Speedometer(screen_size)

    def blit_HUD(self, window):
        self.speedometer.blit_speedometer(window)
