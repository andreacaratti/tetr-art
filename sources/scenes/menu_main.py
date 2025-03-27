#Projet : Tetr'Art
#Auteurs : Andrea CARATTI, Mohamad KARANOUH, Issam MOUTAWAKKIL, Raphael BRICAUD, Ulysse LEONARD SCHWARZ

import math
import copy
import pygame
from os import path
from config import base_path
from engine.scenes import *

PARALLAX_INTENSITY = 15

def ease_in_out(t, fac=2):
    if t >= 0:
        return t ** fac
    else:
        return -((-t) ** fac)

class Menu(Scene):
    def __init__(self, game):
        '''
        On initialise la scène manuellement au le lancement du jeu
        '''
        pass
        #self.load(game, {})
        

    def load(self, game, scene_arguments):
        super().load(game, scene_arguments)
        self.time = 0

        # Main Title
        logo_path = path.join(base_path,"data","img","logo","tetr-art_logo_x4.png")
        self.logo_image = UIImage(27, 125, 746, 200, logo_path)
        self.ui_manager.add_element(self.logo_image)

        # Background
        self.bg_color = (130,130,200) # Default background color
        bg_path = path.join(base_path,"data","img","ui","bg_main.png")
        self.bg_image = pygame.image.load(bg_path)
        self.bg_image = pygame.transform.scale(self.bg_image, (2*self.game.vh + 2*PARALLAX_INTENSITY, self.game.vh + 2*PARALLAX_INTENSITY))
        self.mouse_x = 0 # Parallax effect
        self.mouse_y = 0 
        self.mouse_pos = Vector2(0,0)

        # Buttons Callbacks/Actions
        def button_callback_play():
            self.game.change_scene("Selection", True)
        def button_callback_settings():
            self.game.change_scene("Settings", True)
        def button_callback_quit():
            self.game.quit = True

        # Buttons Texture
        btn_normal = path.join(base_path,"data","img","ui","btn_main_normal.png")
        btn_normal_image = pygame.image.load(btn_normal)
        btn_hover = path.join(base_path,"data","img","ui","btn_main_hover.png")
        btn_hover_image = pygame.image.load(btn_hover)

        # Buttons Font
        font_path = path.join(base_path,"data","fonts","ChakraPetch-Bold.ttf")
        btn_font = pygame.font.Font(font_path, int(40 * self.game.vh/1000))

        # Buttons
        btn_size = (int(400 * self.game.vh/1000), int(80 * self.game.vh/1000))
        btn_padding_y = 0.6*self.game.vh

        button_play = UIButton( int((self.game.vw-btn_size[0])/2), btn_padding_y, btn_size[0], btn_size[1], "Jouer", btn_font, btn_normal_image, btn_hover_image, font_color=(0,0,0))
        button_play.set_callback(button_callback_play)
        button_settings = UIButton( int((self.game.vw-btn_size[0])/2), btn_padding_y + 0.1*self.game.vh, btn_size[0], btn_size[1], "Paramètres", btn_font, btn_normal_image, btn_hover_image, font_color=(0,0,0))
        button_settings.set_callback(button_callback_settings)
        button_quit = UIButton( int((self.game.vw-btn_size[0])/2), btn_padding_y + 0.2*self.game.vh, btn_size[0], btn_size[1], "Quitter", btn_font, btn_normal_image, btn_hover_image, font_color=(0,0,0))
        button_quit.set_callback(button_callback_quit)

        self.ui_manager.add_element(button_play)
        self.ui_manager.add_element(button_settings)
        self.ui_manager.add_element(button_quit)

        self.game.sound_manager.change_music("music1")
        
    def update(self, dt):
        self.time += dt

        #self.logo_image.set_position(x=27, y= 125-int(math.cos(self.time/2)*25) )
        self.mouse_pos = self.mouse_pos*0.95*(1-dt) + Vector2(self.mouse_x, self.mouse_y)*0.05
        if self.time > 10:
            return
            #y=max(0, math.cos((self.time-10)/5))
            #self.bg_color = (130*y,130*y,200*y)


    def draw(self, screen):
        screen.fill(self.bg_color) # default background
        screen.blit(self.bg_image, self.bg_image.get_rect(topleft=(-0.5*self.game.vh - ease_in_out(self.mouse_pos.x, 1.5)*PARALLAX_INTENSITY, -PARALLAX_INTENSITY -ease_in_out(self.mouse_pos.y, 1.5)*PARALLAX_INTENSITY))) # image background
        color = (190,190,190)
        screen.blit(pygame.font.Font(None, 16).render("Maquette Jeu - Puzzle et Tetris", True, color), (620, 780))
        super().draw(screen)

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pygame.MOUSEMOTION:
            self.mouse_x = (event.pos[0]*2 / self.game.vw - 1)
            self.mouse_y = (event.pos[1]*2 / self.game.vh - 1)