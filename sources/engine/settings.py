#Projet : Tetr'Art
#Auteurs : Andrea CARATTI, Mohamad KARANOUH, Issam MOUTAWAKKIL, Raphael BRICAUD, Ulysse LEONARD SCHWARZ

import pygame

class KeyInput():
    def __init__(self, name: str, keys: list, display:str = ""):
        self.name = name
        self.display = display
        self.keys = keys
    
    def isPressed(self, event):
        return event.key in self.keys

class UserConfig:
    def __init__(self):
        self.SIZE_FACTOR = 1.0
        self.inputs:dict[str, KeyInput] = {
            "left" : KeyInput(name="left", keys=[pygame.K_LEFT, pygame.K_a], display="Déplacer à gauche"),
            "right" : KeyInput(name="right", keys=[pygame.K_RIGHT, pygame.K_d], display="Déplacer à droite"),
            "down" : KeyInput(name="down", keys=[pygame.K_DOWN, pygame.K_s], display="down"),
            "rotate" : KeyInput(name="rotate", keys=[pygame.K_r], display="Tourner")
        }