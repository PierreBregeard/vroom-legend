import pygame.sprite
import math


class Car(pygame.sprite.Sprite):

    def __init__(self, idx, img, start_pos):
        super().__init__()
        self.car_id = idx
        self.velocity = 0
        self.angle = 0

        size = 30
        self.image = pygame.transform.scale(img, (size, size))
        self.orig_image = self.image
        self.rect = self.image.get_rect(center=start_pos)

    def update(self, visual_rotation=True):
        angle_rad = math.radians(self.angle)
        velY = self.velocity * math.cos(angle_rad)
        velX = self.velocity * math.sin(angle_rad)
        if visual_rotation:
            self.image = pygame.transform.rotozoom(self.orig_image, self.angle, 1)
        self.rect = self.image.get_rect(center=(self.rect.centerx - velX, self.rect.centery - velY))
