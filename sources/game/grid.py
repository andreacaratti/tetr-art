#Projet : Tetr'Art
#Auteurs : Andrea CARATTI, Mohamad KARANOUH, Issam MOUTAWAKKIL, Raphael BRICAUD, Ulysse LEONARD SCHWARZ

import pygame
from constants import PIXEL_D_SIZE, GRID_BORDER
from pygame import Vector2
from game.pieces import *

class grid():
    def __init__(self, width, height):
        '''
        Initialize the grid with the given width and height.
        - width (int): Width of the grid.
        - height (int): Height of the grid.
        '''
        self.width = width
        self.height = height
        self.position = Vector2() # Position on screen
        self.matrix = [[None for _ in range(width)] for _ in range(height)]

    @property
    def raw_size(self):
        return Vector2(self.width * PIXEL_D_SIZE, self.height * PIXEL_D_SIZE)

    def draw(self, screen, size_factor, placing:Piece = None):
        # Ombre pour indiquer où va tomber la pièce
        if placing and placing.placed==False:
            drag_offset = placing.column_offset*PIXEL_D_SIZE*size_factor + round(placing.drag_screen_offset[0]/(PIXEL_D_SIZE*size_factor))*PIXEL_D_SIZE*size_factor #+placing.drag_screen_offset[0]
            drag_offset = max(0, min(drag_offset, self.raw_size[1]*size_factor - placing.matrix_size[0]*PIXEL_D_SIZE*size_factor))
            color = (100, 100, 100, 100)
            rect = pygame.rect.Rect(
                                self.position.x + drag_offset,
                                self.position.y,
                                placing.matrix_size[0]*PIXEL_D_SIZE*size_factor,
                                self.raw_size[1]*size_factor
                            )
            transparent_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            transparent_surface.fill(color)
            screen.blit(transparent_surface, (rect.x, rect.y))

        # Lignes de la grille
        color = (200, 200, 200)
        for x in range(0, int(self.width+1)):
            pygame.draw.rect(screen, 
                             color,
                             pygame.rect.Rect(
                                 self.position.x + x*PIXEL_D_SIZE*size_factor,
                                 self.position.y,
                                 GRID_BORDER*size_factor,
                                 self.raw_size.y*size_factor
                             ))
        for y in range(0, int(self.height+1)):
            pygame.draw.rect(screen, 
                             color,
                             pygame.rect.Rect(
                                 self.position.x,
                                 self.position.y + y*PIXEL_D_SIZE*size_factor,
                                 self.raw_size.x*size_factor,
                                 GRID_BORDER*size_factor
                             ))

    def place_piece(self, piece:Piece):
        piece_width, piece_height = piece.matrix_size

        valid = False
        row = 0
        for row_start in range(0, self.height-piece_height+1, 1):
            if self.height-row_start < piece_height:
                break  # Not enough space vertically

            row_valid = True

            for y in range(piece_height):
                grid_y = int(row_start + y)
                for x in range(piece_width):
                    grid_x = int(piece.column_offset + x)
                    if grid_x >= self.width or (piece.matrix[y][x] and self.matrix[grid_y][grid_x]):
                        row_valid = False
                        break
                if not row_valid:
                    break
            if row_valid:
                valid=True
                row=row_start
            else:
                break

        if valid:
            # Place the piece
            for y in range(piece_height):
                grid_y = row + y
                for x in range(piece_width):
                    grid_x = piece.column_offset + x
                    if piece.matrix[y][x] != None:
                        self.matrix[grid_y][grid_x] = piece.id
            return True, row# - piece_height + 1

        return False, None
    
    def remove_piece(self, id):
        for y in range(self.height):
            for x in range(self.width):
                if self.matrix[y][x] == id:
                    self.matrix[y][x] = None