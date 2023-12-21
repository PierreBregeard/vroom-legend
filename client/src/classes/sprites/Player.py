from .Car import Car
import math
import pygame


class Player(Car):
    horse_power = .02
    max_speed = 10
    max_speed_reverse = 4
    brake_power = .08
    drag_power = .005
    turn_power = 3

    def __init__(self, idx, img, start_pos):
        super().__init__(idx, img, start_pos)

    def handle_keys_press(self, keys):
        if keys[pygame.K_UP] or keys[pygame.K_z]:
            self.handle_throttle()
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.handle_brake()
        else:
            self.idle()

        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            self.turn()
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.turn(False)
        self.update()

    def handle_throttle(self):
        if self.velocity >= 0:
            self.throttle()
        else:
            self.brake()

    def handle_brake(self):
        if self.velocity > 0:
            self.brake()
        else:
            self.throttle(True)

    def throttle(self, reverse=False):
        max_speed = self.max_speed if not reverse else self.max_speed_reverse
        self.velocity = max_speed - (max_speed - abs(self.velocity)) * math.exp(-self.horse_power)
        if reverse:
            self.velocity *= -1

    def brake(self):
        if self.velocity > 0:
            self.velocity -= self.brake_power
        elif self.velocity < 0:
            self.velocity += self.brake_power

    def idle(self):
        if self.velocity > 0.3:
            self.velocity -= self.drag_power
            self.velocity -= self.drag_power
        elif self.velocity < -0.3:
            self.velocity += self.drag_power
            self.velocity += self.drag_power
        else:
            self.velocity = 0
            self.velocity = 0

    def turn(self, left=True):
        turn_power = self.turn_power * (self.velocity / self.max_speed)

        if left:
            self.angle = (self.angle + turn_power) % 360
        else:
            self.angle = (self.angle - turn_power) % 360
