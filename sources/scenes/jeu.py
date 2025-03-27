#Projet : Tetr'Art
#Auteurs : Andrea CARATTI, Mohamad KARANOUH, Issam MOUTAWAKKIL, Raphael BRICAUD, Ulysse LEONARD SCHWARZ

import pygame
from constants import PIXEL_D_SIZE, PIXEL_BORDER, CANVA_BORDER, GRID_OFFSET, PLACING_BORDER, PLACING_BD_COLOR, PLACING_Y_OFFSET, PLACING_VALID, FALLING_SPEED, BG_COLOR, STOCK_BORDER, STOCK_PC_SIZE, PULSE_SPEED, BG_ALPHA
from pygame import Vector2
from math import cos
from engine.scenes import *
from game.pieces import *
from game.grid import *#)))qws<é""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""zaq"""
from game.timer import Timer
from os import path
from config import base_path
from levels.levels_list import *

class Jeu(Scene):
    def __init__(self, game):
        '''
        On n'initialise pas la scène dès le lancement du jeu, lorsque cette classe est instanciée
        '''
        pass

    def load(self, game, scene_arguments:dict):
        super().load(game, scene_arguments)

        # Récupération du niveau chargé
        self.level = scene_arguments.get("loaded_lvl")
        if not len(self.level.pieces) > 0:
            # Si les pièces n'ont pas été générées on ignore le niveau
            self.level = None

        # Éléments nécessaires au fonctionnement de base du jeu
        self.camera_offset = Vector2(0,0)
        self.camera_pos = (100,-100)
        self.grid = grid(int(self.level.size.x), int(self.level.size.y)) if self.level else grid(6,7)
        self.last_click = 0 # dernier click
        self.popup_elements:dict[str, any] = None # Popup de fin
        self.time = 0
        self.score = 0
        self.tutorial = False

        # Menu pour interchanger les pièces
        self.stock_rects: dict[int, list] = {} # numéro dans l'ordre de la pièce (int), liste des rects pour les collisions (list)

        # Réglages
        self.settings = game.settings # Réglages du jeu
        self.TRUE_SIZE_FACTOR = 0.5 # Propotion de l'interface
        if self.level:
            self.TRUE_SIZE_FACTOR = self.settings.SIZE_FACTOR * self.level.SIZE_FACTOR
            self.tutorial = self.level.tutorial

        # Première pièce
        if self.level:
            self.placing = self.level.pieces[0]
            self.level.pieces.remove(self.placing)
        else:
            self.placing = Piece()
        self.placed_pieces:Piece = []

        # Ressources
        btn_normal = path.join(base_path,"data","img","ui","btn_main_normal.png")
        font_path = path.join(base_path,"data","fonts","PressStart2P-Regular.ttf")
        self.arcade_font = pygame.font.Font(font_path,  30)

        # Chronomètre
        duration = 120
        countdown=True

        if self.level:
            duration = self.level.duration
        if duration == 0:
            countdown=False

        self.timer = Timer(duration=duration, countdown=countdown)
        self.timer.start()

        # Affichage du chronomètre
        self.timer_display = Label(self.game.vw/2,35,"0000", self.arcade_font, color=(0,0,0), text_align="C")
        self.timer_bg = UIImage(240,20,320,64,btn_normal)
        self.ui_manager.add_element(self.timer_bg)
        self.ui_manager.add_element(self.timer_display)

        # Bouton retour
        def button_callback_back():
            self.game.change_scene("Menu", True)
        button_back = UIButton(10,10,75,30, "Retour", pygame.font.Font(None,24), (70,130,180), (100,149,237), (30,144,255))
        button_back.set_callback(button_callback_back)
        self.ui_manager.add_element(button_back)

        # Fond du tableau
        self.canva = None
        self.canva_color = (230, 230, 230)
        if self.level:
            self.canva = self.level.canva_preview
            self.canva = pygame.transform.scale(self.canva, (self.grid.width*PIXEL_D_SIZE*self.TRUE_SIZE_FACTOR, self.grid.height*PIXEL_D_SIZE*self.TRUE_SIZE_FACTOR))
            self.canva.set_alpha(BG_ALPHA)
            self.canva_color = self.level.canva_color or (230, 230, 230)

        ### TEST ###
        #self.end_popup("game_won")
        #self.end_popup("game_lost")
        ### TEST ###

        self.game.sound_manager.change_music("music2")
        # Fonctionnement du jeu
        self.active = True
    
    def draw(self, screen):
        '''
        '''
        screen.fill(BG_COLOR)

        #self.camera_offset = Vector2(screen.get_height()/2, screen.get_width()/2) - self.camera_pos # Inutile
        if self.level:
            self.TRUE_SIZE_FACTOR = self.settings.SIZE_FACTOR * self.level.SIZE_FACTOR
        else :
            self.TRUE_SIZE_FACTOR = self.settings.SIZE_FACTOR * 0.5

        # corner + offset
        self.grid.position = Vector2(0, self.game.vh - self.grid.raw_size.y*self.TRUE_SIZE_FACTOR) + Vector2(GRID_OFFSET, -GRID_OFFSET)*self.TRUE_SIZE_FACTOR

        # Bordure de la grille
        pygame.draw.rect(screen, 
                         (240,186,57), 
                         pygame.Rect(self.grid.position.x - CANVA_BORDER*self.TRUE_SIZE_FACTOR, 
                                     self.grid.position.y - CANVA_BORDER*self.TRUE_SIZE_FACTOR, 
                                     (self.grid.raw_size.x + 2*CANVA_BORDER) * self.TRUE_SIZE_FACTOR, 
                                     (self.grid.raw_size.y + 2*CANVA_BORDER) * self.TRUE_SIZE_FACTOR))

        # Fond du tableau
        canva_rect = pygame.Rect(self.grid.position.x, 
                                 self.grid.position.y, 
                                 self.grid.raw_size.x * self.TRUE_SIZE_FACTOR, 
                                 self.grid.raw_size.y * self.TRUE_SIZE_FACTOR)
        pygame.draw.rect(screen, self.canva_color, canva_rect)
        if self.canva:
            screen.blit(self.canva, canva_rect)
        # Grille
        self.grid.draw(screen, self.TRUE_SIZE_FACTOR, self.placing)

        # On affiche toutes les pièces placées
        for pc in self.placed_pieces:
            screen_offset = self.grid.position
            x_offset = screen_offset[0] + pc.position[0] * PIXEL_D_SIZE * self.TRUE_SIZE_FACTOR
            y_offset = screen_offset[1] + pc.position[1] * PIXEL_D_SIZE * self.TRUE_SIZE_FACTOR - pc.falling_animation_offset
            for y, row in enumerate(pc.matrix):
                for x, cell in enumerate(row):
                    if cell != None:
                        if self.level and self.level.image and pc.correct_pos != None:
                            
                            pixel_positon = pc.matrix[y][x]

                            sub_image = self.level.image[int(pixel_positon.y)][int(pixel_positon.x)]  # Récupérer la surface pré-découpée
                            rotated_image = pygame.transform.rotate(sub_image, (-pc.rotation*90))

                            screen.blit(rotated_image, 
                                        (x_offset + (x * PIXEL_D_SIZE * self.TRUE_SIZE_FACTOR), 
                                        y_offset + (y * PIXEL_D_SIZE * self.TRUE_SIZE_FACTOR)))
                            
                            if pc.correct_pos != pc.position or pc.rotation != 0:
                                #opacity = 100 * max(0, cos(((self.time/5)%2 - 1)*3.14))
                                opacity = 100 * max(0, cos((self.time-pc.time_placed)*PULSE_SPEED))
                                red_surface = pygame.surface.Surface(rotated_image.get_size(), pygame.SRCALPHA)
                                red_surface.fill((255,0,0,int(opacity)))

                                screen.blit(red_surface, 
                                            (x_offset + (x * PIXEL_D_SIZE * self.TRUE_SIZE_FACTOR), 
                                             y_offset + (y * PIXEL_D_SIZE * self.TRUE_SIZE_FACTOR)))

                        else:
                            color = pc.color
                            pygame.draw.rect(screen, color, pygame.Rect(x_offset + (x * PIXEL_D_SIZE * self.TRUE_SIZE_FACTOR), y_offset + (y * PIXEL_D_SIZE * self.TRUE_SIZE_FACTOR), (PIXEL_D_SIZE - PIXEL_BORDER) * self.TRUE_SIZE_FACTOR, (PIXEL_D_SIZE - PIXEL_BORDER) * self.TRUE_SIZE_FACTOR))

        # On affiche la pièce à placer avec presque la même logique que pour les pièces placées
        if self.placing:
            drag_offset = Vector2(self.placing.drag_screen_offset[0],0)
            #if self.placing.drag_screen_offset[1] > PLACING_VALID:
            #    drag_offset = Vector2(self.placing.drag_screen_offset[0], PLACING_VALID*self.TRUE_SIZE_FACTOR)
            drag_offset.y = max(0, min(self.placing.drag_screen_offset[1], PLACING_VALID))
            screen_offset = self.grid.position + Vector2(0, -PLACING_Y_OFFSET*self.TRUE_SIZE_FACTOR) + Vector2(self.placing.column_offset, -self.placing.matrix_size[1])*PIXEL_D_SIZE*self.TRUE_SIZE_FACTOR + drag_offset
            
            # Bordure de la pièce
            for y, row in enumerate(self.placing.matrix):
                for x, cell in enumerate(row):
                    if cell != None:
                        pygame.draw.rect(screen, PLACING_BD_COLOR, pygame.Rect(
                                screen_offset.x + (x * PIXEL_D_SIZE - PLACING_BORDER)*self.TRUE_SIZE_FACTOR,
                                screen_offset.y + (y * PIXEL_D_SIZE - PLACING_BORDER)*self.TRUE_SIZE_FACTOR,
                                (PIXEL_D_SIZE - PIXEL_BORDER + 2*PLACING_BORDER)*self.TRUE_SIZE_FACTOR, 
                                (PIXEL_D_SIZE - PIXEL_BORDER + 2*PLACING_BORDER)*self.TRUE_SIZE_FACTOR))

            # Affichage de la pièce
            for y, row in enumerate(self.placing.matrix):
                for x, cell in enumerate(row):
                    if cell != None:
                        if self.level and self.level.image and self.placing.correct_pos != None:

                            #pixel_positon, rotation = self.placing.get_pixel_position_after_rotation(correct_pos, x, y)
                            pixel_positon = self.placing.matrix[y][x]

                            sub_image = self.level.image[int(pixel_positon.y)][int(pixel_positon.x)]  # Récupérer la surface pré-découpée
                            rotated_image = pygame.transform.rotate(sub_image, (-self.placing.rotation*90))

                            x_offset = screen_offset.x + x * PIXEL_D_SIZE * self.TRUE_SIZE_FACTOR
                            y_offset = screen_offset.y + y * PIXEL_D_SIZE * self.TRUE_SIZE_FACTOR

                            screen.blit(rotated_image, 
                                        (x_offset, 
                                         y_offset))
                        else:
                            color = self.placing.color
                            pygame.draw.rect(screen, color,pygame.Rect(
                                screen_offset.x + x * PIXEL_D_SIZE * self.TRUE_SIZE_FACTOR,
                                screen_offset.y + y * PIXEL_D_SIZE * self.TRUE_SIZE_FACTOR,
                                (PIXEL_D_SIZE - PIXEL_BORDER)*self.TRUE_SIZE_FACTOR, 
                                (PIXEL_D_SIZE - PIXEL_BORDER)*self.TRUE_SIZE_FACTOR))

        if self.level:        
            # Menu pour interchanger les pièces
            # On l'appel "stock"
            self.stock_rects = {}

            stock_position = Vector2(self.game.vw - (PIXEL_D_SIZE*6*STOCK_PC_SIZE + GRID_OFFSET - CANVA_BORDER)*self.TRUE_SIZE_FACTOR,
                                     self.grid.position[1] - CANVA_BORDER*self.TRUE_SIZE_FACTOR)
            stock_size = Vector2(PIXEL_D_SIZE*6*STOCK_PC_SIZE*self.TRUE_SIZE_FACTOR, 
                                 (self.grid.raw_size[1] + 2*CANVA_BORDER)*self.TRUE_SIZE_FACTOR)

            pygame.draw.rect(screen, (255,255,255), pygame.rect.Rect(
                            stock_position.x,
                            stock_position.y,
                            stock_size.x,
                            stock_size.y), 
                            int(max(1, (STOCK_BORDER*self.TRUE_SIZE_FACTOR)+1))) # Affichage de la bordure du stock
            
            stock_start_poss = self.game.vw - (PIXEL_D_SIZE*3*STOCK_PC_SIZE + GRID_OFFSET - CANVA_BORDER)*self.TRUE_SIZE_FACTOR

            stock_pcs_yoffset = 0
            for index, next_pc in enumerate(self.level.pieces):
                screen_position = Vector2((stock_start_poss - next_pc.matrix_size[0]/2 * PIXEL_D_SIZE * self.TRUE_SIZE_FACTOR*STOCK_PC_SIZE), (self.grid.position.y + stock_pcs_yoffset))# + index * 4 * PIXEL_D_SIZE * self.TRUE_SIZE_FACTOR*STOCK_PC_SIZE))

                if screen_position.y + next_pc.matrix_size[1]*PIXEL_D_SIZE*self.TRUE_SIZE_FACTOR*STOCK_PC_SIZE > stock_position.y + stock_size.y:
                    break

                self.stock_rects[index] = list()
                #self.stock_rects[index]

                # Bordure de la pièce
                for y, row in enumerate(next_pc.matrix):
                    for x, cell in enumerate(row):
                        if cell != None:
                            pygame.draw.rect(screen, PLACING_BD_COLOR, pygame.Rect(
                                screen_position[0] + (x * PIXEL_D_SIZE - PLACING_BORDER) * self.TRUE_SIZE_FACTOR*STOCK_PC_SIZE,
                                screen_position[1] + (y * PIXEL_D_SIZE - PLACING_BORDER) * self.TRUE_SIZE_FACTOR*STOCK_PC_SIZE,
                                (PIXEL_D_SIZE - PIXEL_BORDER + 2*PLACING_BORDER) * self.TRUE_SIZE_FACTOR*STOCK_PC_SIZE +1, 
                                (PIXEL_D_SIZE - PIXEL_BORDER + 2*PLACING_BORDER) * self.TRUE_SIZE_FACTOR*STOCK_PC_SIZE +1))

                # Affichage de la pièce texturée
                for y, row in enumerate(next_pc.matrix):
                    for x, cell in enumerate(row):
                        if cell != None:
                            if self.level.image and next_pc.correct_pos != None:
                                
                                pixel_positon = next_pc.matrix[y][x]

                                sub_image = self.level.image[int(pixel_positon.y)][int(pixel_positon.x)]  # Récupérer la surface pré-découpée
                                rotated_image = pygame.transform.rotate(sub_image, (-next_pc.rotation*90))
                                scaled_image = pygame.transform.scale(rotated_image, 
                                                                      ((PIXEL_D_SIZE-PIXEL_BORDER) * self.TRUE_SIZE_FACTOR*STOCK_PC_SIZE, 
                                                                       (PIXEL_D_SIZE-PIXEL_BORDER) * self.TRUE_SIZE_FACTOR*STOCK_PC_SIZE))

                                screen.blit(scaled_image, 
                                            (screen_position[0] + (x * PIXEL_D_SIZE * self.TRUE_SIZE_FACTOR*STOCK_PC_SIZE), 
                                             screen_position[1] + (y * PIXEL_D_SIZE * self.TRUE_SIZE_FACTOR*STOCK_PC_SIZE)))
                                
                                # Rect pour les collisions/clicks
                                rect = pygame.Rect(
                                        screen_position[0] + x * PIXEL_D_SIZE * self.TRUE_SIZE_FACTOR*STOCK_PC_SIZE,
                                        screen_position[1] + y * PIXEL_D_SIZE * self.TRUE_SIZE_FACTOR*STOCK_PC_SIZE,
                                        (PIXEL_D_SIZE - PIXEL_BORDER) * self.TRUE_SIZE_FACTOR*STOCK_PC_SIZE, 
                                        (PIXEL_D_SIZE - PIXEL_BORDER) * self.TRUE_SIZE_FACTOR*STOCK_PC_SIZE)
                                self.stock_rects[index].append(rect)
                                
                stock_pcs_yoffset += (next_pc.matrix_size[1] + 1) * PIXEL_D_SIZE*self.TRUE_SIZE_FACTOR*STOCK_PC_SIZE
                        
        super().draw(screen) # Pour l'interface

    def update(self, dt):
        '''
        '''
        self.time += dt

        self.timer.update(dt)
        minutes, seconds = divmod(int(self.timer.elapsed), 60)
        
        self.timer_display.set_text(f"{minutes:02}:{seconds:02}")

        if self.timer.ended and self.active:
            print(True)
            self.end_check()

        # Animation de chute des pièces
        for pc in self.placed_pieces:
            if pc.falling_animation_offset != 0:
                pc.falling_animation_offset = max(0, pc.falling_animation_offset - FALLING_SPEED*dt)


    def end_check(self):
        self.score = 0
        if self.level:
            self.score = round(self.level.check(self.placed_pieces), 2) * 100

        if self.timer.ended:
            self.active = False
        else:
            if self.score == 100 :
                self.active = False
        if not self.active:
            if self.score == 100:
                self.handle_event("game_won")
            else:
                self.handle_event("game_lost")
            self.timer.stop()

    def end_popup(self, event):
        image_path = None
        if event=="game_won":
            image_path = path.join(base_path,"data","img","ui","game_won.png")
        elif event=="game_lost":
            image_path = path.join(base_path,"data","img","ui","game_lost.png")
        else:
            return
        
        self.popup_elements = {
            "image" : UIImage(self.game.vw/2 - self.game.vh/2, 0, 
                              self.game.vh, self.game.vh, 
                              image_path),
            "text" : Label(self.game.vw/2, self.game.vh*0.71, 
                           f"{int(round(self.score, 0))}%", 
                           self.arcade_font, color=(0,0,0), 
                           text_align="C")
        }

        self.ui_manager.add_element(self.popup_elements["image"])
        self.ui_manager.add_element(self.popup_elements["text"])

    
    # Gestion du choix de la pièce sélectionnée

    def next_piece(self):
        '''
        Cette fonction décide de la prochaine pièce à placer.
        On suit l'ordre de
        '''
        last_c_offset = int(self.placing.column_offset) # Better for User Experience
        if self.level and len(self.level.pieces) > 0:
            self.placing = self.level.pieces[0]
            self.placing.reset()
            self.level.pieces.remove(self.placing)
            self.move_piece(last_c_offset)
        elif not self.level:
            self.placing = Piece()
            self.move_piece(last_c_offset)
        else:
            self.placing = None
            if self.level:
                self.end_check()

    def swap_piece(self, index):
        if self.level:
            c_offset = 0
            new_placing = self.level.pieces[index]
            if new_placing:
                if self.placing:
                    c_offset = int(self.placing.column_offset)
                    self.level.pieces[index] = self.placing
                else:
                    self.level.pieces.remove(new_placing)
                self.placing = new_placing
                self.move_piece(c_offset) # Better for User Experience

    
    # Fonctions dédiées au glissé-déposé :

    def drag_start(self, event):
        self.placing.drag = True
        self.placing.drag_start = event.pos

    def drag(self, event):
        self.placing.drag_screen_offset = list(a - b for a, b in zip(event.pos, self.placing.drag_start))

    def drag_stop(self, event):
        # Fin du glisser, positionnement de la pièce
        self.placing.drag = False
        # On ne considère le glisser seulement si la pièce est maintenue plus de 200ms.
        is_drag = (pygame.time.get_ticks()-self.last_click)>=200

        if is_drag:            
            # Calcul de la nouvelle position en colonne de la pièce
            drag_offset = round((self.placing.drag_screen_offset[0]) / (self.grid.width*PIXEL_D_SIZE*self.TRUE_SIZE_FACTOR) * self.grid.width )
            self.move_piece(drag_offset)

            if self.placing.drag_screen_offset[1] > PLACING_VALID:
                # Si le glisser-déposser sur l'axe y est suffisant pour placer la pièce
                if self.try_place():
                    self.placing.drag_screen_offset = [0,0]
                    self.next_piece()
                else:
                    self.placing.drag_screen_offset = [0,0]
            else:
                self.placing.drag_screen_offset = [0,0]
        else:
            self.placing.drag_screen_offset = [0,0]


    # Fonction dédiée à la gestion de la pièce actuellement sélectionnée :

    def touching(self, event, placing_position):
        # Vérification si la souris clique sur une cellule de la pièce à placer
        for y in range(0, len(self.placing.matrix)):
            for x in range(0, len(self.placing.matrix[y])):
                if self.placing.matrix[y][x] != None:
                    rect = pygame.Rect(
                        (placing_position.x + (PIXEL_D_SIZE*x*self.TRUE_SIZE_FACTOR)),
                        (placing_position.y + (PIXEL_D_SIZE*y*self.TRUE_SIZE_FACTOR)),
                        (PIXEL_D_SIZE - PIXEL_BORDER) * self.TRUE_SIZE_FACTOR, 
                        (PIXEL_D_SIZE - PIXEL_BORDER) * self.TRUE_SIZE_FACTOR)
                    if rect.collidepoint(event.pos):
                        return True
        return False

    def move_piece(self, offset):
        '''
        Cette fonction permet de déplacer lattéralement la pièce sélectionnée
        '''
        new_offset = self.placing.column_offset + offset
        self.placing.column_offset = max(0, min(new_offset, (self.grid.width - self.placing.matrix_size[0])))

    def try_place(self):
        valid, valid_pos = self.grid.place_piece(self.placing)
        if valid and valid_pos>=0:
            # Si la position est valide
            self.placing.placed = True
            self.placing.position = [self.placing.column_offset, valid_pos]

            self.placing.falling_animation_offset = valid_pos*PIXEL_D_SIZE*self.TRUE_SIZE_FACTOR
            self.placing.time_placed = self.time

            self.placed_pieces.append(self.placing)

            return True
        else:
            return False


    def on_click(self, event):
        '''
        '''
        # Gestion du double click
        new_click = pygame.time.get_ticks()
        double_click = (new_click-self.last_click)<=500
        self.last_click = new_click

        if self.placing:
            # Calcul des offsets pour la pièce en train d'être placée
            placing_position = self.grid.position + Vector2(0, -PLACING_Y_OFFSET*self.TRUE_SIZE_FACTOR) + Vector2(self.placing.column_offset, -self.placing.matrix_size[1])*PIXEL_D_SIZE*self.TRUE_SIZE_FACTOR
            touching = self.touching(event, placing_position)
            if touching:
                if double_click:
                    self.last_click = 0 #Pour éviter des rotations en continue, toujours 2 clicks
                    self.placing.rotate()
                    return # Retour anticipé
                else:
                    self.drag_start(event)
                    return # Retour anticipé

        # Vérification si la souris clique sur une pièce déjà placée pour la supprimer
        for pc in self.placed_pieces:
            
            if pc.collide(origin=self.grid.position, collid_pos=event.pos,size_factor=self.TRUE_SIZE_FACTOR):
                self.grid.remove_piece(id=pc.id)
                self.placed_pieces.remove(pc)

                c_offset = 0
                #Si une pièce est déjà
                if self.placing and self.level:
                    c_offset = int(self.placing.column_offset)
                    self.level.pieces.insert(0, self.placing)

                pc.reset()
                self.placing = pc
                self.move_piece(c_offset)
                # On peut retirer de la liste seulement parce qu'il y a un retour anticipé, sinon il y aurait des erreurs d'indexation.
                return # Retour anticipé
            
        for index, next_pcs in self.stock_rects.items():
            if isinstance(next_pcs, list):
                for rect in next_pcs:
                    if isinstance(rect, pygame.rect.Rect):
                        if rect.collidepoint(event.pos):
                            self.swap_piece(index=index)
                            return # Retour anticipé


    def handle_event(self, event):

        if self.active :
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.on_click(event)

            elif self.placing:     
                if event.type == pygame.MOUSEBUTTONUP:
                    self.drag_stop(event)
                    
                elif self.placing.drag and event.type == pygame.MOUSEMOTION:
                    self.drag(event)

                elif event.type == pygame.KEYDOWN and not self.placing.drag:
                    #if event.key in self.settings.keys["rotate"]:#event.key == pygame.K_r:
                    #    self.placing.rotate()
                    if self.settings.inputs["rotate"].isPressed(event):
                        self.placing.rotate()
                    elif self.settings.inputs["left"].isPressed(event):
                        self.move_piece(-1)
                    elif self.settings.inputs["right"].isPressed(event):
                        self.move_piece(1)
                    elif self.settings.inputs["down"].isPressed(event):
                        if self.try_place():
                            self.placing.drag_screen_offset = [0,0]
                            self.next_piece()

        elif event=="game_won" or event=="game_lost":
            self.end_popup(event)
        
        super().handle_event(event)
