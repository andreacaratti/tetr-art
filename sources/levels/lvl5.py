#Projet : Tetr'Art
#Auteurs : Andrea CARATTI, Mohamad KARANOUH, Issam MOUTAWAKKIL, Raphael BRICAUD, Ulysse LEONARD SCHWARZ

### NIVEAU QUATRIEME ###
from config import base_path
from game.pieces import *
from game.level import *
from os import path

class Lvl5Warrior(level):
    def __init__(self):
        super().__init__()
        self.size = Vector2(20,20)
        self.SIZE_FACTOR = 0.26
        self.PIXELS_PER_TILE = 3
        self.duration = 720

        self.canva_color = (120, 120, 120)
    
    def load_image(self):
        level_image_path = path.join(base_path,"data","img","levels","lvl5_Warrior_Pixel.png")
        image = pygame.image.load(level_image_path).convert()
        self.split_image(image=image)

        level_preview_path = path.join(base_path,"data","img","levels","lvl5_Warrior_Pixel.png")
        self.canva_preview = pygame.image.load(level_preview_path).convert()