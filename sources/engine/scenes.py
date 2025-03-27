#Projet : Tetr'Art
#Auteurs : Andrea CARATTI, Mohamad KARANOUH, Issam MOUTAWAKKIL, Raphael BRICAUD, Ulysse LEONARD SCHWARZ

from pygame import event as _event
from ui.ui_manager import UIManager
from ui.ui_elements import *

class Scene:
    def __init__(self, game):
        self.game = game
        self._loaded = False
        #self.load(game)

    def load(self, game, scene_arguments={}):
        """
        Initialisation des scènes peut être manuelle
        """
        self.scene_arguments = scene_arguments if scene_arguments else {}
        self.game = game
        self.ui_manager = UIManager()
        self._loaded = True

    def update(self, dt):
        pass

    def draw(self, screen):
        self.ui_manager.draw(screen)

    def handle_event(self, event):
        """
        Gère les événements.
        """
        if isinstance(event, _event.Event):
            self.ui_manager.handle_event(event)