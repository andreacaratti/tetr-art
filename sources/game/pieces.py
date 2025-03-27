#Projet : Tetr'Art
#Auteurs : Andrea CARATTI, Mohamad KARANOUH, Issam MOUTAWAKKIL, Raphael BRICAUD, Ulysse LEONARD SCHWARZ

import uuid
import random
import colorsys
import pygame
from constants import PIXEL_D_SIZE
from pygame import Vector2

SIZE_FACTOR = 0.5

class Piece():
    '''
    Représente une pièce dans le jeu. Gère la matrice, la couleur, et l'état de placement.
    '''
    def __init__(self, matrix=None, id=None, correct_pos=None):
        self.id = id or uuid.uuid1()

        # Lorsque la pièce est placée
        self.position = [0,0]
        self.correct_pos = correct_pos if correct_pos is not None else Vector2(0,0)
        self.placed = False
        self.time_placed = 0

        self.color = self.generate_color() # Couleur par défaut
        self.falling_animation_offset = 0 # Décalage sur l'axe y pour l'animation de chute lors du placement

        self.column_offset = 0
        self.rotation = 0 # De 0 à 3 inclus

        # Glisser
        self.drag = False
        self.drag_start = (0,0)
        self.drag_screen_offset = [0,0]

        self.last_click = 0 # Utilisation pour le double clic

        self.matrix = [[1,None],[1,None],[1,1]]
        if matrix:
            # Pour être sûr qu'il s'agit bien d'une liste de listes
            self.matrix = [list(t) for t in matrix]

    def reset(self):
        self.position = [0,0]
        self.placed = False
        self.drag = False
        self.drag_start = (0,0)
        self.drag_screen_offset = [0,0]
        self.column_offset = 0
        self.last_click = 0
        self.falling_animation_offset = 0
        self.time_placed = 0

    @property
    def matrix_size(self):
        return len(self.matrix[0]), len(self.matrix)

    @staticmethod
    def generate_color():
        hue = random.uniform(0, 360)
        r, g, b = colorsys.hls_to_rgb(hue / 360.0, 0.61, 0.70)
        return (int(r * 255), int(g * 255), int(b * 255))
        
    def get_rects(self, origin, size_factor=SIZE_FACTOR):
        rects = []
        if self.placed:
            x_offset = origin[0] + self.position[0] * PIXEL_D_SIZE * size_factor
            y_offset = origin[1] + self.position[1] * PIXEL_D_SIZE * size_factor
            for y, row in enumerate(self.matrix):
                for x, cell in enumerate(row):
                    if cell != None:
                        rects.append(
                            pygame.Rect(
                                x_offset + (x * PIXEL_D_SIZE * size_factor),
                                y_offset + (y * PIXEL_D_SIZE * size_factor),
                                (PIXEL_D_SIZE) * size_factor, 
                                (PIXEL_D_SIZE) * size_factor
                            )
                        )
        return rects
    
    def collide(self, origin, collid_pos, size_factor=SIZE_FACTOR) -> bool:
        for rect in self.get_rects(origin, size_factor):
            if rect.collidepoint(collid_pos):
                return True
        return False
    
    def rotate(self):
        '''
        Fait pivoter la matrice de la pièce de 90° dans le sens horaire,
        tout en s'assurant que la pièce reste dans le coin inférieur gauche.
        '''
        # Transpose puis inverse les lignes pour effectuer une rotation
        rotated_matrix = list(zip(*self.matrix[::-1]))
        self.rotation = (self.rotation + 1) if self.rotation < 3 else 0
        
        # Mettre à jour la matrice
        self.matrix = rotated_matrix#adjusted_matrix

    def convert_matrix(self):
        for y, row in enumerate(self.matrix):
            for x, cell in enumerate(row):
                if cell != None:
                    self.matrix[y][x] = self.correct_pos + Vector2(x,y)

    def mouse_down(self):
        pass
    def mouse_up(self):
        pass