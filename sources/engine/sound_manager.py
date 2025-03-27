#Projet : Tetr'Art
#Auteurs : Andrea CARATTI, Mohamad KARANOUH, Issam MOUTAWAKKIL, Raphael BRICAUD, Ulysse LEONARD SCHWARZ

import pygame
from threading import Thread
from time import sleep
from os import path
from constants import FADEOUT_T

class SoundManager():
    def __init__(self, volume_sfx=1, volume_music=1):
        try:
            pygame.mixer.init()
            self.audio_available = True
        except pygame.error:
            print("Mixer initialization error. Sound will be disabled.")
            self.audio_available = False

        self.volume_sfx = volume_sfx
        self.volume_music = volume_music
        
        self.next_name:str = None # Next music
        self.actual = None # Actual music
        self.loop = False
        self.fade_thread = None

        self.sfx: dict[str, pygame.mixer.Sound] = {
            #"sfx1" : pygame.mixer.Sound()
        }
        self.musics: dict[str, str] = { # Music path
            #"music1" : "path.join()"
        }

    def play_sound(self, name:str, loop=False):
        if not self.audio_available:
            return
        
        sound = self.sfx.get(name)
        if sound:
            loop_int = -1 if loop else 0
            sound.play(loops=loop_int)
        else:
            print(f"Sound {name} not found in sound effects list.")

    def next_music(self):
        if not self.audio_available:
            return
        
        new_music_path = self.musics.get(self.next_name)
        if not new_music_path or not path.exists(new_music_path):
            print(f"Can't load, music not found : {self.next_name}")
            return
        
        try:
            pygame.mixer.music.load(new_music_path)
        except pygame.error as error:
            print(f"Can't load music : {error}")
            return
        loop_int = -1 if self.loop else 0
        pygame.mixer.music.play(loops=loop_int)

        self.actual = self.next_name

    def stop_music(self):
        if not self.audio_available:
            return
        pygame.mixer.music.fadeout(FADEOUT_T)
        self.actual = None

    def __change_music(self):
        """Thread to manage fading and change music.
        """
        if not self.audio_available:
            self.fade_thread = None
            return
        
        sleep(FADEOUT_T/1000)
        self.next_music()
        self.fade_thread = None # Allows creation of a new thread

    def change_music(self, name:str, loop:bool=True):
        if not self.audio_available:
            return

        if not self.musics.get(name):
            print(f"music not found in musics : {name}")
            return
        
        if name == None or name == "":
            self.stop_music()
            return

        # Replaces the next music
        self.next_name = name
        self.loop = loop

        if self.actual == None:
            self.next_music()
            return
        
        # Fade out
        pygame.mixer.music.fadeout(FADEOUT_T)
        
        # Pygame can only play one music at a time
        # No need to wait again if the music is already stopping, and there's only one next music at a time

        if self.fade_thread and self.fade_thread.is_alive():
            return # Prevent multiple threads
        
        self.fade_thread = Thread(target=self.__change_music)
        self.fade_thread.start()