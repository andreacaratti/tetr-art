#Projet : Tetr'Art
#Auteurs : Andrea CARATTI, Mohamad KARANOUH, Issam MOUTAWAKKIL, Raphael BRICAUD, Ulysse LEONARD SCHWARZ

from constants import PIXEL_D_SIZE, PIXEL_BORDER
from pygame import Vector2
from game.pieces import *

class level():
    def __init__(self):
        self.size:Vector2 = Vector2(0,0) # matrix size
        self.image = []
        self.pieces:Piece = []
        self.duration = 120
        self.tutorial = False

        self.canva_preview = None
        self.canva_color = (230, 230, 230)

        self.SIZE_FACTOR = 0.5
        self.PIXELS_PER_TILE = 3

    def check(self, placed_pieces:list):
        count = 0
        total_pieces = self.size.x * self.size.y / 4
        remaining_pieces = len(self.pieces)

        for piece in placed_pieces:
            if piece.position == piece.correct_pos and piece.rotation == 0:
                count += 1

        return (count/(total_pieces+remaining_pieces)) if (total_pieces+remaining_pieces) > 0 else 0  
    
    def split_image(self, image):
        
        image_width, image_height = image.get_size()
        self.image = []

        for y in range(0, image_height, self.PIXELS_PER_TILE):
            row = []
            for x in range(0, image_width, self.PIXELS_PER_TILE):
                # Extraire une zone de IMG_RES x IMG_RES
                sub_surface = pygame.Surface((self.PIXELS_PER_TILE, self.PIXELS_PER_TILE), pygame.SRCALPHA)
                sub_surface.blit(image, (0, 0), (x, y, self.PIXELS_PER_TILE, self.PIXELS_PER_TILE))
                
                # Agrandir la surface
                scaled_surface = pygame.transform.scale(
                    sub_surface, 
                    ((PIXEL_D_SIZE-PIXEL_BORDER)*self.SIZE_FACTOR, 
                     (PIXEL_D_SIZE-PIXEL_BORDER)*self.SIZE_FACTOR))
                row.append(scaled_surface)
            self.image.append(row)

    def load_image(self):
        self.image = []
