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

    fake_rotation = 0

    is_hand_braking = False

    def __init__(self, idx, img, start_pos, start_angle):
        super().__init__(idx, img, start_pos, start_angle)

    def handle_keys_press(self, keys):
        if keys[pygame.K_UP] or keys[pygame.K_z]:
            self.handle_throttle()
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.handle_brake()
        else:
            self.idle()

        self.is_hand_braking = keys[pygame.K_SPACE]

        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            self.turn()
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.turn(False)

    def handle_throttle(self):
        if self.velocity >= 0:
            self.throttle()
        else:
            self.brake()

    def handle_brake(self):
        if self.velocity > 0:
            self.brake()
        else:
            self.throttle(reverse=True)

    def throttle(self, reverse=False):
        self.velocity = self.max_speed - (self.max_speed - abs(self.velocity)) * math.exp(-self.horse_power)
        if reverse:
            if self.velocity > self.max_speed_reverse:
                self.velocity = self.max_speed_reverse
            self.velocity *= -1

    def brake(self):
        if self.velocity > 0:
            self.velocity -= self.brake_power
        elif self.velocity < 0:
            self.velocity += self.brake_power

    def idle(self):
        self.velocity *= 1 - self.drag_power

    def turn(self, left=True):
        turn_power = self.turn_power * (self.velocity / self.max_speed)

        if self.is_hand_braking:
            fake_rotation = turn_power * .5
            if not left:
                fake_rotation *= -1
            self.fake_rotation += fake_rotation
            self.fake_rotation = max(-30, min(30, self.fake_rotation))
            self.idle()
            turn_power += abs(self.fake_rotation) / 30

        if left:
            self.angle = (self.angle + turn_power) % 360
        else:
            self.angle = (self.angle - turn_power) % 360

    def update(self):
        self.cached_position = (self.rect.centerx, self.rect.centery)

        if not self.is_hand_braking and self.fake_rotation != 0:
            # self.angle += self.fake_rotation
            # self.fake_rotation = 0

            fake_rotation_threshold = 1
            if abs(self.fake_rotation) < fake_rotation_threshold:
                self.fake_rotation = 0
            else:
                drift_recuperation = 2
                if self.fake_rotation > 0:
                    self.fake_rotation -= drift_recuperation
                else:
                    self.fake_rotation += drift_recuperation


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


        print(self.fake_rotation)
        self.image = pygame.transform.rotozoom(self.orig_image, self.angle + self.fake_rotation, 1)


        new_center = self.rect.centerx - velX, self.rect.centery - velY
        self.rect = self.image.get_rect(center=new_center)
