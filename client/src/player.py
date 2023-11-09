import pygame.sprite


class Player(pygame.sprite.Sprite):

    def __init__(self, window):
        self.vel = 2
        self.rect = pygame.Rect(0, 0, 40, 20)
        self.window = window
        self.rect.center = window.get_rect().center

        # voir plus tard
        super().__init__()
        #self.sprite_sheet = pygame.image.load("ressources/sprites/Cars.jpg")
        #self.image = self.get_image(0, 0)
        #self.rect = self.image.get_rect()

    def get_image(self,x,y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0,0), (x, y, 32, 32))
        return image

    def getCenter(self):
        return self.rect.center

    def drawPlayer(self, keys):
        self.rect.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.vel
        self.rect.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * self.vel

        self.rect.x %= self.window.get_width()
        self.rect.y %= self.window.get_height()

        pygame.draw.rect(self.window, (255, 0, 0), self.rect)

    def drawRealPlayer(self):
        return

