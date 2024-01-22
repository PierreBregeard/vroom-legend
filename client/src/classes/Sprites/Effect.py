from pygame.sprite import Sprite


class Effect(Sprite):
    def __init__(self, duration):
        super().__init__()
        self.duration = duration
        self.timer = 0

    def update(self):
        self.timer += 1
        if self.timer >= self.duration:
            self.kill()
