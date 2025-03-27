#Projet : Tetr'Art
#Auteurs : Andrea CARATTI, Mohamad KARANOUH, Issam MOUTAWAKKIL, Raphael BRICAUD, Ulysse LEONARD SCHWARZ

### Utilisé pour la conception du générateur ###

import pygame
import random
import colorsys
from pygame import *

PXL_SIZE = 50 #Constante pour l'affichage. Non important à la logique

class Piece():
    def __init__(self, id=0, matrix=None, correct_pos=Vector2(0,0)):
        self.id = id
        self.matrix = matrix if matrix else [[1,None],[1,None],[1,1]]
        self.correct_pos = correct_pos
        self.color = self.generate_color()

    @staticmethod
    def generate_color():
        """
        Donne une couleur pour l'affichage
        """
        hue = random.uniform(0, 360)
        r, g, b = colorsys.hls_to_rgb(hue / 360.0, 0.61, 0.70)
        return (int(r * 255), int(g * 255), int(b * 255))
    
    def draw(self, screen):
        """
        Affichage pour le débogage
        """
        offset = self.correct_pos * PXL_SIZE
        for y, row in enumerate(self.matrix):
            for x, cell in enumerate(row):
                if cell != None:
                    pygame.draw.rect(screen, 
                                     self.color, 
                                     pygame.Rect(
                                         int(offset.x + x*PXL_SIZE), 
                                         int(offset.y + y*PXL_SIZE), 
                                         PXL_SIZE-1, 
                                         PXL_SIZE-1))
    
    def rotate(self):
        """
        Fait pivoter la matrice de la pièce de 90° dans le sens horaire
        """
        # Transpose puis inverse les lignes pour effectuer une rotation
        rotated_matrix = list(zip(*self.matrix[::-1]))   
        # Mettre à jour la matrice
        self.matrix = rotated_matrix
