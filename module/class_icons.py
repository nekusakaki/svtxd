from PIL import Image
import os


class ClassIcons:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls, *args, **kwargs)

        return cls._instance

    def __init__(self):
        self.icons = self.generate_icons()

    def generate_icons(self):
        icons = {}
        folder_path = '../images/class_icons/'

        for root, directories, files in os.walk(folder_path):
            for file in files:
                if '.png' in file:
                    clan = file.replace('.png', '')
                    image = Image.open(folder_path + file)
                    icons[clan] = image

        return icons

    def get_icon(self, clan):
        clan = clan.lower()
        return self.icons[clan]
