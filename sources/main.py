#Projet : Tetr'Art
#Auteurs : Andrea CARATTI, Mohamad KARANOUH, Issam MOUTAWAKKIL, Raphael BRICAUD, Ulysse LEONARD SCHWARZ

from engine.game_engine import *
from scenes.menu_selection import *
from scenes.menu_settings import *
from scenes.test_scene import *
from scenes.menu_main import *
from scenes.loading import *
from scenes.jeu import *

game = Game(800, 800)

game.sound_manager.musics = {
    "music1" : path.join(base_path,"data","sounds","musics","music_tukish_march.ogg"),
    "music2" : path.join(base_path,"data","sounds","musics","music_tukish_march.ogg")
}

game.scenes = {
    "Menu": Menu(game),
    "Selection": Selection_Menu(game),
    "Settings": Settings_Menu(game),
    "Loading": Loading_Screen(game),
    "Jeu": Jeu(game),
    "Test": Test_Scene(game)
}
game.change_scene("Menu", True)

game.run() 