#Projet : Tetr'Art
#Auteurs : Andrea CARATTI, Mohamad KARANOUH, Issam MOUTAWAKKIL, Raphael BRICAUD, Ulysse LEONARD SCHWARZ

from engine.scenes import *

class Settings_options(Scene):
    def __init__(self, game):
        self.load(game, {})

        def button_callback_w():
            pass
        def button_callback_a():
            pass
        def button_callback_s():
            pass
        def button_callback_d():
            pass
        
    def load(self, game, scene_arguments):
        super().load(game, scene_arguments)

    def draw(self, screen):
        screen.fill((0,0,0))
        super().draw(screen)

    def _handle_event(self, event):
        super().handle_event(event)