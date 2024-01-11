import pygame.sprite
import math


class Car(pygame.sprite.Sprite):

    def __init__(self, idx, img, start_pos, start_angle):
        super().__init__()
        self.car_id = idx
        self.velocity = 0
        self.angle = start_angle

        self.velXToAdd = 0
        self.velYToAdd = 0

        VEHICLE_WIDTH = 30
        ratio = img.get_size()[0] / VEHICLE_WIDTH
        size = img.get_size()[0] // ratio, img.get_size()[1] // ratio
        self.image = pygame.transform.scale(img, size)

        self.orig_image = self.image
        self.rect = self.image.get_rect(center=start_pos)
        self.cached_position = start_pos

    def update(self):
        self.cached_position = (self.rect.centerx, self.rect.centery)

        velocity_threshold = 0.1
        if abs(self.velocity) < velocity_threshold:
            self.velocity = 0

        angle_rad = math.radians(self.angle)

        velY = self.velocity * math.cos(angle_rad) + self.velYToAdd
        self.velYToAdd = velY - round(velY)
        velY = round(velY)
        velX = self.velocity * math.sin(angle_rad) + self.velXToAdd
        self.velXToAdd = velX - round(velX)
        velX = round(velX)

        self.image = pygame.transform.rotozoom(self.orig_image, self.angle, 1)

        new_center = self.rect.centerx - velX, self.rect.centery - velY
        self.rect = self.image.get_rect(center=new_center)

    def crash(self):
        self.rect = self.image.get_rect(center=(self.cached_position[0], self.cached_position[1]))
        self.velocity = -(self.velocity / 3.5)
