import pygame.sprite
import math


class Car(pygame.sprite.Sprite):
    vel = 0
    rotation_angle = 0

    def __init__(self, car_id, img, start_pos):
        super().__init__()
        self.x, self.y = start_pos
        self.car_id = car_id

        size = 40
        self.img = pygame.transform.scale(img, (size, size))

    def add_vel_to_pos(self):
        angle_rad = math.radians(self.rotation_angle)

        velY = self.vel * math.cos(angle_rad)
        velX = self.vel * math.sin(angle_rad)

        self.y -= velY
        self.x -= velX

    def blit_car_to_surface(self, surface):
        rotated_image = pygame.transform.rotate(self.img, self.rotation_angle)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(center=(self.x, self.y)).center)
        surface.blit(rotated_image, new_rect)
