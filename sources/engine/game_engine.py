#Projet : Tetr'Art
#Auteurs : Andrea CARATTI, Mohamad KARANOUH, Issam MOUTAWAKKIL, Raphael BRICAUD, Ulysse LEONARD SCHWARZ

from engine.sound_manager import SoundManager
from engine.scenes import Scene
from engine.settings import *
from config import base_path
from os import path
import pygame
import sys


class Game:
    def __init__(self, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        pygame.display.set_caption("Maquette Jeu")

        # Units #
        # Inspired by css
        self.vw = self.screen.get_width()
        self.vh = self.screen.get_height()
        # ##### #

        self.settings = UserConfig()
        self.sound_manager = SoundManager()
        self.scenes: dict[str, Scene] = {}
        self.current_scene = None

        self.quit = False

    def change_scene(self, scene_name, reload_scene, scene_arguments={}):
        '''
        Cette fonction permet de changer de scène.
        '''
        scene = self.scenes.get(scene_name)
        if scene:
            self.current_scene = scene
            if reload_scene:
                self.current_scene.load(self, scene_arguments)

    def run(self):
        '''
        Cette fonction lance la boucle principale du jeu
        '''
        while not self.quit:
            dt = self.clock.tick(60)/1000
            # Limite le rafraichissement à 60 IPS

            # Gestion des évènenements
            for event in pygame.event.get():
                if self.current_scene and self.current_scene._loaded:
                    # Délégation de la gestion des autres évènements à la scène
                    self.current_scene.handle_event(event)
                if event.type == pygame.QUIT:
                    self.quit = True

            if self.current_scene and self.current_scene._loaded:
                self.current_scene.update(dt)
                
                self.current_scene.draw(self.screen)

            # Rafraichissement de l'écran
            pygame.display.flip()
        
        # Quand la boucle principale est terminée
        pygame.quit()
        sys.exit()
        