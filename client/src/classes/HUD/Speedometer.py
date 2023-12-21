from ..ResourcePath import RelativePath
import pygame


class Speedometer:
    speed = 0

    def __init__(self, screen_size, max_speed):
        self.screen_size = screen_size
        self.max_speed = max_speed

        SIZE = 500
        ratio = SIZE / screen_size[0]

        needle_path = RelativePath.resource_path("ressources\\sprites\\dependencies\\needle.png")
        self.needle = pygame.image.load(needle_path).convert_alpha()
        needle_size = self.needle.get_size()
        self.needle = pygame.transform.scale(
            self.needle,
            (int(needle_size[0] * ratio), int(needle_size[1] * ratio))
        )

        speedometer_path = RelativePath.resource_path("ressources\\sprites\\dependencies\\speedometer.png")
        self.speedometer = pygame.image.load(speedometer_path).convert_alpha()
        speedometer_size = pygame.image.load(speedometer_path).get_size()
        self.speedometer = pygame.transform.scale(
            self.speedometer,
            (int(speedometer_size[0] * ratio), int(speedometer_size[1] * ratio))
        )

    def blit_speedometer(self, window):
        speedometer_rect = self.speedometer.get_rect()
        speedometer_rect.center = (
            self.screen_size[0] - self.speedometer.get_size()[0] // 2.5,
            self.screen_size[1] - self.speedometer.get_size()[1] // 3.2
        )

        angle = 140
        angle -= abs(self.speed) / self.max_speed * 280

        needle_rotated = pygame.transform.rotate(self.needle, angle)
        needle_rect = needle_rotated.get_rect(center=speedometer_rect.center)

        window.blit(self.speedometer, speedometer_rect)
        window.blit(needle_rotated, needle_rect)
