import pyscroll
import pytmx


class World():

    def __init__(self, screenSize):
        tmx_data = pytmx.util_pygame.load_pygame("../Maps/FirstMap.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, screenSize)
        map_layer.zoom=1.8
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)

    def drawWorld(self, window, center):
        self.group.center(center)
        self.group.draw(window)

