#Projet : Tetr'Art
#Auteurs : Andrea CARATTI, Mohamad KARANOUH, Issam MOUTAWAKKIL, Raphael BRICAUD, Ulysse LEONARD SCHWARZ

### NIVEAU TUTORIEL ###
from config import base_path
from game.pieces import *
from game.level import *
from os import path

class Lvl0MonaLisa(level):
    def __init__(self):
        super().__init__()
        self.size = Vector2(10,10)
        self.SIZE_FACTOR = 0.4 # 0.4
        self.PIXELS_PER_TILE = 3
        self.duration = 0 # Unlimited time
        self.tutorial = True
    
    def load_image(self):
        level_image_path = path.join(base_path,"data","img","levels","lvl0_MonaLisa_64c.png")
        image = pygame.image.load(level_image_path).convert()
        self.split_image(image=image)

        level_preview_path = path.join(base_path,"data","img","levels","lvl0_CanvaPreview.png")
        self.canva_preview = pygame.image.load(level_preview_path).convert()