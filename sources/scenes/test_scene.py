#Projet : Tetr'Art
#Auteurs : Andrea CARATTI, Mohamad KARANOUH, Issam MOUTAWAKKIL, Raphael BRICAUD, Ulysse LEONARD SCHWARZ

import copy
from os import path
from engine.scenes import *

class Test_Scene(Scene):
    def __init__(self, game):
        self.load(game, {})

    def load(self, game, scene_arguments):
        super().load(game, scene_arguments)
        self.bg_color = (50,50,50)

        Value = SliderValue(0.5)
        Slider = UISlider(100, 100, 200, 5, (100,100,100), UIThumb(12, (200,200,200), (150,150,150)), Value)
        self.ui_manager.add_element(Slider)
        
    def draw(self, screen):
        screen.fill(self.bg_color)
        super().draw(screen)

    def handle_event(self, event):
        
        super().handle_event(event)