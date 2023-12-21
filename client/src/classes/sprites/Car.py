import pygame.sprite
import math


class Car(pygame.sprite.Sprite):

    def __init__(self, idx, img, start_pos):
        super().__init__()
        self.car_id = idx
        self.velocity = 0
        self.angle = 0

        VEHICLE_WIDTH = 30
        ratio = img.get_size()[0] / VEHICLE_WIDTH
        size = img.get_size()[0] // ratio, img.get_size()[1] // ratio
        self.image = pygame.transform.scale(img, size)

        self.orig_image = self.image
        self.rect = self.image.get_rect(center=start_pos)
        self.cached_position = (0, 0)

    def update(self):
        # cached position store the position before move in case we
        # undo move because of a collision
        self.cached_position = (self.rect.centerx, self.rect.centery )
        angle_rad = math.radians(self.angle)
        velY = self.velocity * math.cos(angle_rad)
        velX = self.velocity * math.sin(angle_rad)
        self.image = pygame.transform.rotozoom(self.orig_image, self.angle, 1)
        self.rect = self.image.get_rect(center=(self.rect.centerx - velX, self.rect.centery - velY))

    def undo_move(self):
        self.rect = self.image.get_rect(center=(self.cached_position[0], self.cached_position[1]))
