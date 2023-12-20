from PIL import Image
from .ResourcePath import RelativePath


class ColorCar:

    def __init__(self, car_base_path, car_roof_path):
        self.car_base_path = car_base_path
        self.car_roof_path = car_roof_path

    def __set_color(self, img, color_add):
        r, g, b = color_add
        pixels = img.load()
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                if pixels[i, j][3] != 0:  # if not transparent
                    pixels[i, j] = (
                        min(pixels[i, j][0] + r, 255),
                        min(pixels[i, j][1] + g, 255),
                        min(pixels[i, j][2] + b, 255),
                        pixels[i, j][3]
                    )

    def set_base_color(self, color_add):
        img = Image.open(self.car_base_path)
        self.__set_color(img, color_add)

    def set_roof_color(self, color_add):
        img = Image.open(self.car_base_path)
        self.__set_color(img, color_add)
