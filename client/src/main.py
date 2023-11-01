import pygame
import pyscroll
import pytmx

pygame.init()

screenHeight = 500
screenWidth = 700
screenSize = (screenWidth, screenWidth)

window = pygame.display.set_mode(screenSize)
clock = pygame.time.Clock()

rect = pygame.Rect(0, 0, 20, 20)
rect.center = window.get_rect().center

# Initialisation de la map en format .tmx
tmx_data = pytmx.util_pygame.load_pygame("../Maps/FirstMap.tmx")
map_data = pyscroll.data.TiledMapData(tmx_data)
map_layer = pyscroll.orthographic.BufferedRenderer(map_data, screenSize)

# Dessiner le groupe de calques
group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)


vel = 5

run = True
while run:
    clock.tick(60)
    group.draw(window)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # if event.type == pygame.KEYDOWN:
        #     print(pygame.key.name(event.key))

    keys = pygame.key.get_pressed()

    rect.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * vel
    rect.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * vel

    rect.x %= window.get_width()
    rect.y %= window.get_height()
    pygame.draw.rect(window, (255, 0, 0), rect)
    pygame.display.flip()

pygame.quit()
