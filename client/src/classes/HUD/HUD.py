from .Speedometer import Speedometer


class HUD:

    def __init__(self, screen_size, max_speed):
        self.speedometer = Speedometer(screen_size, max_speed)

    def blit_HUD(self, window):
        self.speedometer.blit_speedometer(window)
