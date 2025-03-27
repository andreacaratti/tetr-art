#Projet : Tetr'Art
#Auteurs : Andrea CARATTI, Mohamad KARANOUH, Issam MOUTAWAKKIL, Raphael BRICAUD, Ulysse LEONARD SCHWARZ

from game.generator.pieces_list import *
from game.pieces import *
from pygame import Vector2
import random

# CONSTANTES
ATTEMPS_MAX = 25
ATTEMPS_RISK = 18
ATTEMPS_MODERATE = 10

class Generator():
    def __init__(self, height, width, randomness=4):
        self.height = height
        self.width = width

        self.pieces = [] # Pieces actuellement placée dans l'ordre, si possible self.pieces doit contenir des pièces de la class piece()
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        self.max_pieces = self.height*self.width // 4
        self.placing_position = Vector2(0,height-1) # On démare à la dernière ligne, comme on commence à 0 ymax=height-1
        self.id_count = 1 # Compteur d'id, correspond à l'ordre des pièces, très important.
        self.randomness = randomness # Nombres de pièces placées aléatoirement au début de la génération. Permet d'éviter une grille trop logique.

        self.areas = [[None for _ in range(self.width)] for _ in range(self.height)]

    def generate(self):
        """
        Cette méthode lance la génération
        """
        attemps = 0
    
        while attemps <= ATTEMPS_MAX:

            if not (self.height*self.width % 4 == 0):
                return
            
            self.initial_randomness()
            self.placing_position = Vector2(0,self.height-1)

            # Le sens de génération doit être de gauche à droite, de bas en haut
            while len(self.pieces) < self.max_pieces:
                self.place_random()

                self.placing_position = self.placing_position + Vector2(1,0)
                if self.placing_position.x > self.width-1:
                    self.placing_position.x = 0
                    self.placing_position.y = self.placing_position.y - 1
                if self.placing_position.y < 0:
                    break
            
            attemps += 1
            # Si une grille n'a pas pu être totalement être remplie, on réessaie jusqu'à MAX_ATTEMPS essaies.
            if len(self.pieces) < self.max_pieces:
                self.pieces = []
                self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
                self.placing_position = Vector2(0,self.height-1)
                self.id_count = 1
                self.areas = [[None for _ in range(self.width)] for _ in range(self.height)]

                # On réduit l'aléatoire au bout de la moitié des essaies aléatoires
                if attemps >= ATTEMPS_RISK: 
                    self.randomness = 0
                if (attemps >= ATTEMPS_MODERATE) and (self.randomness > 2):
                    self.randomness = 2
            else:
                return True
        return False



    def initial_randomness(self):
        """
        Cette fonction permet d'éviter une grille trop logique en placant quelles pièces à des positions aléatoires
        """
        for _ in range(self.randomness):
            attemps = 0
            succeded = False
            while (succeded==False) and (attemps <= ATTEMPS_MAX):
                self.placing_position = Vector2(random.randint(0, self.width-1),random.randint(0, self.height-1))
                if self.place_random():
                    succeded = True
                attemps += 1



    def check_placement(self, last_piece:Piece):
        empty_count = 0 # Nombre d'espaces vides
        for row in self.grid:
            for cell in row:
                if cell == None:
                    empty_count += 1

        if empty_count == 0:
            return True
        
        self.areas = [[None for _ in range(self.width)] for _ in range(self.height)]

        # Creation des areas. 
        # Ces zones correspondent au zones vides laissées par la pièces. 
        # Si un zone n'est pas divisible par 4 alors la pièce ne permet pas remplir correctement la grille de tétrominos.
        creared_area_count = 1 # Identifiant 
        for y, row in enumerate(last_piece.matrix):
            for x, cell in enumerate(row):
                if cell != None:
                    self.place_area(
                        creared_area_count, 
                        (last_piece.correct_pos + Vector2(x, y) + Vector2(-1,0))) #Left
                    creared_area_count += 1
                    self.place_area(
                        creared_area_count, 
                        (last_piece.correct_pos + Vector2(x, y) + Vector2(1,0))) #Right
                    creared_area_count += 1
                    self.place_area(
                        creared_area_count, 
                        (last_piece.correct_pos + Vector2(x, y) + Vector2(0,1))) #Top
                    creared_area_count += 1
                    self.place_area(
                        creared_area_count, 
                        (last_piece.correct_pos + Vector2(x, y) + Vector2(0,-1))) #Bottom
                    creared_area_count += 1

        areas_count = 0 # Nombres d'espace occupés par des areas.

        # Dans le cas où aucune zone vide n'est adjacente
        for row in self.areas:
            for cell in row:
                if cell != None:
                    areas_count += 1
        if areas_count == 0:
            return True

        # Expension des areas
        attemps = 0 #Nombre d'essaies max. évite de rester coincé à l'infini si une zone vide n'est pas adjacente
        while (areas_count < empty_count):
            self.expand_areas()
            areas_count = 0
            for row in self.areas:
                for cell in row:
                    if cell != None:
                        areas_count += 1
            attemps += 1
            if attemps > empty_count*2: # 2 fois pour être sûr
                break # Sorti d'un boucle infini
        self.expand_areas()
        self.expand_areas()

        areas_dict = {}
        for row in self.areas:
            for cell in row:
                if cell != None:
                    if not cell in areas_dict:
                        areas_dict[cell] = 0
                    areas_dict[cell] += 1
        correct_placement = True
        for size in areas_dict.values():
            if size % 4 != 0:
                correct_placement = False

        self.areas = []

        return correct_placement 

    def replace_area(self, old_id, new_id):
        for y, row in enumerate(self.areas):
            for x, cell in enumerate(row):
                if cell == old_id:
                    self.areas[y][x] = new_id

    def place_area(self, area_id, position):
        #is inside
        if not (0 <= position.x < self.width):
            return
        if not (0 <= position.y < self.height):
            return
        if self.grid[int(position.y)][int(position.x)] != None:
            return
        if self.areas[int(position.y)][int(position.x)] == area_id:
            return
        
        if self.areas[int(position.y)][int(position.x)] != None:
            self.replace_area(
                old_id = self.areas[int(position.y)][int(position.x)], 
                new_id = area_id)
            return
        
        self.areas[int(position.y)][int(position.x)] = area_id
        return
    
    def expand_areas(self):
        for y, row in enumerate(self.areas):
            for x, cell_id in enumerate(row):
                if cell_id != None:
                    self.place_area(
                        cell_id, 
                        (Vector2(x, y) + Vector2(-1,0))) #Left
                    self.place_area(
                        cell_id, 
                        (Vector2(x, y) + Vector2(1,0))) #Right
                    self.place_area(
                        cell_id, 
                        (Vector2(x, y) + Vector2(0,1))) #Top
                    self.place_area(
                        cell_id, 
                        (Vector2(x, y) + Vector2(0,-1))) #Bottom
        


    def place_piece(self, position, matrix, id, piece_name=""):
        # Logique de placement dans self.grid, permet d'indiquer les carreax pris de la grille (aka grid)
        rotations_possibilities = [0,1,2,3] # Rotation possibles pour la pièce
        while len(rotations_possibilities) > 0:
            rotation = random.choice(rotations_possibilities) # On choisi une rotation aléatoire

            new_matrix = matrix
            for _ in range(rotation):
                new_matrix = rotate_matrix(new_matrix)
        
            is_valid_placement = True
            adjusted_position = position + Vector2(0,1) - Vector2(0, len(new_matrix))

            # On vérifie di on peut placer la pièce
            if position.x + len(new_matrix[0]) - 1> self.width - 1:
                is_valid_placement = False
            if position.y - len(new_matrix) + 1 < 0:
                is_valid_placement = False
            if is_valid_placement == True:
                for y, row in enumerate(new_matrix):
                    for x, cell in enumerate(row):
                        if cell != None:
                            if self.grid[int(adjusted_position.y) + y][int(adjusted_position.x) + x] != None:
                                is_valid_placement = False
                        if is_valid_placement == False:
                            break
                    if is_valid_placement == False:
                        break
            
            if is_valid_placement==True:
                valid_piece = Piece(id=id, matrix=new_matrix, correct_pos=adjusted_position)
                self.pieces.append(valid_piece)

                for y, row in enumerate(new_matrix):
                    for x, cell in enumerate(row):
                        if cell != None:
                            self.grid[int(adjusted_position.y) + y][int(adjusted_position.x) + x] = id

                if self.check_placement(valid_piece) == True:
                    return True
                else:
                    self.remove_piece(id)
                    self.pieces.remove(valid_piece)

            rotations_possibilities.remove(rotation)# On retire la rotation aléatoire si elle n'est pas valide

        return False

    def remove_piece(self, id):
        #Retire de la grille
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell==id:
                    self.grid[y][x]=None

    def place_random(self):
        # séléction aléatoire d'une pièce + retrait de la liste si on doit rechoisir car la pièce ne correspond pas
        pieces_possibilities = list(pieces_list.keys())
        while len(pieces_possibilities) > 0:
            piece_name = random.choice(pieces_possibilities)

            if self.place_piece(self.placing_position, pieces_list[piece_name], self.id_count, piece_name):
                self.id_count += 1
                return True

            pieces_possibilities.remove(piece_name)
        return False
