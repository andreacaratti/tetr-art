#Projet : Tetr'Art
#Auteurs : Andrea CARATTI, Mohamad KARANOUH, Issam MOUTAWAKKIL, Raphael BRICAUD, Ulysse LEONARD SCHWARZ

from pygame import event as _event
from ui.ui_elements import *

class UIManager:
    def __init__(self):
        self.elements = []

    def add_element(self, element):
        if not isinstance(element, UIElement):
            # On ignore tout élément qui n'est pas dérivé de UIElement
            return
        self.elements.append(element)

    def remove_element(self, element):
        self.elements.remove(element)

    def draw(self, screen):
        for element in self.elements:
            if element.visible:
                element.draw(screen)

    def handle_event(self, event):
        if isinstance(event, _event.Event):
            for element in self.elements:
                    element.handle_event(event)