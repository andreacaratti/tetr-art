#Projet : Tetr'Art
#Auteurs : Andrea CARATTI, Mohamad KARANOUH, Issam MOUTAWAKKIL, Raphael BRICAUD, Ulysse LEONARD SCHWARZ

from engine.scenes import *
from game.level import level
from levels.levels_list import *
from threading import Thread
from game.generator.generator import *
from time import sleep
from random import randint
import copy

class Loading_Screen(Scene):
    def __init__(self, game):
        super().__init__(game)

    def load(self, game, scene_arguments={}):
        super().load(game, scene_arguments)

        self.time = 0
        self.bg_color = (30,30,30)

        loading_txt = Label(x=400, y=400, text="Loading...", font=self.game.font, text_align="C")
        self.ui_manager.add_element(loading_txt)
        self.level_loaded = False
        self.level = None

        self.game.sound_manager.stop_music()

        level_number = scene_arguments.get("lvl")

        if level_number == None: 
            print("Level number Error")
            self.game.change_scene("Menu", True)
            return

        if level_number == 0:
            self.level = Lvl0MonaLisa()
        elif level_number == 1:
            self.level = Lvl1TheDream()
        elif level_number == 2:
            self.level = Lvl2TheStarryNight()
        elif level_number == 3:
            self.level = Lvl3TheScreem()
        elif level_number == 4:
            self.level = Lvl4Kanagawa()
        elif level_number == 5:
            self.level = Lvl5Warrior()
        else:
            self.game.change_scene("Menu", True)
            return

        if self.level == None: 
            print("Level doesn't exists")
            self.game.change_scene("Menu", True)
            return
        
        self.loading_thread = Thread(target=self.load_level)
        self.loading_thread.start()

    def load_level(self):

        self.level.load_image()
        if not len(self.level.image) > 0:
            print("image loading error")

        width = self.level.size.x
        height = self.level.size.y

        self.start_generating(int(width), int(height))

        for pc in self.level.pieces:
            # Convert pieces matrix
            pc.convert_matrix()
            # Give random rotation
            for _ in range(randint(0,3)):
                pc.rotate()

        self.level_loaded = True


    def start_generating(self, width:int, height:int):

        saved_t = self.time
        #print(saved_t)
        gen = Generator(height=height, width=width, randomness=0)
        gen.generate()
        #print(self.time-saved_t)

        self.level.pieces = copy.deepcopy(gen.pieces)
        #self.level.pieces.reverse()

        del gen

        sleep(2)

    def update(self, dt):
        self.time += dt
        if int(self.time) >= 1 and self.level_loaded:
            self.game.change_scene("Jeu", True, {"loaded_lvl":self.level})

    def draw(self, screen):
        screen.fill(self.bg_color)

        super().draw(screen)

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pygame.QUIT:
            pass