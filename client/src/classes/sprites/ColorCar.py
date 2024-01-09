from PIL import Image
from .ResourcePath import RelativePath
from os import makedirs
from shutil import rmtree


class ColorCar:
    tmp_folder = RelativePath.resource_path("ressources\\sprites\\dependencies\\temp")

    def __init__(self):
        self.car_base_img = Image.open(
            RelativePath.resource_path("ressources\\sprites\\dependencies\\player_base.png")
        )
        self.car_roof_img = Image.open(
            RelativePath.resource_path("ressources\\sprites\\dependencies\\player_roof.png")
        )

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
        self.__set_color(self.car_base_img, color_add)

    def set_roof_color(self, color_add):
        self.__set_color(self.car_roof_img, color_add)

    def save_img(self, player_id=""):
        tmp = self.car_base_img.copy()
        tmp.paste(self.car_roof_img, (0, 0), self.car_roof_img)
        makedirs(self.tmp_folder, exist_ok=True)
        path = f"{self.tmp_folder}\\{player_id}player.png"
        tmp.save(path)
        return path

    @staticmethod
    def remove_temp_files():
        rmtree(ColorCar.tmp_folder, ignore_errors=True)
