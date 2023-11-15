from .Car import Car
import math
import pygame


class Player(Car):
    horse_power = .01
    max_speed = 8
    brake_power = .08
    drag_power = .005
    turn_power = 2

    def __init__(self, car_id, img, start_pos):
        super().__init__(car_id, img, start_pos)

    def handle_keys_press(self, keys):
        if keys[pygame.K_UP]:
            self.handle_throttle()
        elif keys[pygame.K_DOWN]:
            self.handle_brake()
        else:
            self.idle()

        if keys[pygame.K_LEFT]:
            self.turn()
        elif keys[pygame.K_RIGHT]:
            self.turn(False)

    def handle_throttle(self):
        if self.vel >= 0:
            self.throttle()
        else:
            self.brake()
        self.add_vel_to_pos()

    def handle_brake(self):
        if self.vel > 0:
            self.brake()
        else:
            self.throttle(True)
        self.add_vel_to_pos()

    def throttle(self, reverse=False):
        self.vel = self.max_speed - (self.max_speed - abs(self.vel)) * math.exp(-self.horse_power)
        if reverse:
            self.vel *= -1

    def brake(self):
        if self.vel > 0:
            self.vel -= self.brake_power
        elif self.vel < 0:
            self.vel += self.brake_power

    def idle(self):
        if self.vel > 0.3:
            self.vel -= self.drag_power
            self.vel -= self.drag_power
        elif self.vel < -0.3:
            self.vel += self.drag_power
            self.vel += self.drag_power
        else:
            self.vel = 0
            self.vel = 0
        self.add_vel_to_pos()

    def turn(self, left=True):
        # turn_power = 2 - (2 - abs(self.vel)) * math.exp(-0.005)

        if self.vel == 0:
            return

        if left:
            self.rotation_angle = (self.rotation_angle + self.turn_power) % 360
        else:
            self.rotation_angle = (self.rotation_angle - self.turn_power) % 360
