#Projet : Tetr'Art
#Auteurs : Andrea CARATTI, Mohamad KARANOUH, Issam MOUTAWAKKIL, Raphael BRICAUD, Ulysse LEONARD SCHWARZ

from os import path
from functools import partial
from config import base_path
from engine.scenes import *

PARALLAX_INTENSITY = 15

def ease_in_out(t, fac=2):
    if t >= 0:
        return t ** fac
    else:
        return -((-t) ** fac)

class Selection_Menu(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.load(game, {})

    def load(self, game, scene_arguments):
        super().load(game, scene_arguments)

        # Units
        vw = self.game.vw
        vh = self.game.vh
        vh_factor = vh/1000 #Les interfaces ont été faites pour une fenêtre de 1000x1000px

        # Background
        self.bg_color = (50,50,50)
        bg_path = path.join(base_path,"data","img","ui","bg_main.png")
        self.bg_image = pygame.image.load(bg_path)
        self.bg_image = pygame.transform.scale(self.bg_image, (2*self.game.vh + 2*PARALLAX_INTENSITY, self.game.vh + 2*PARALLAX_INTENSITY))
        self.mouse_x = 0 # Parallax effect
        self.mouse_y = 0 
        self.mouse_pos = Vector2(0,0)

        # Title
        font_path_1 = path.join(base_path,"data","fonts","ChakraPetch-Bold.ttf")
        font_h1 = pygame.font.Font(font_path_1, int(80 * vh_factor))
        title = Label(x=int(self.game.vw/2), y=int(60*vh_factor), text="JOUER", font=font_h1, color=(255,255,255), text_align="C")
        self.ui_manager.add_element(title)

        # Bouton retour
        def button_callback_back():
            self.game.change_scene("Menu", False)
        button_back = UIButton(300,700,200,50, "Retour", self.game.font, None)
        button_back.set_callback(button_callback_back)
        self.ui_manager.add_element(button_back)

        def button_callback_level_generic(level_id):
            #self.game.change_scene(scene_name="Loading", reload_scene=True, scene_arguments={"lvl":level_id})
            self.create_popup(level_id)

        btn_normal = path.join(base_path,"data","img","ui","btn_selection_normal.png")
        btn_normal_image = pygame.image.load(btn_normal)
        btn_hover = path.join(base_path,"data","img","ui","btn_selection_hover.png")
        btn_hover_image = pygame.image.load(btn_hover)
        font_path = path.join(base_path,"data","fonts","PressStart2P-Regular.ttf")
        self.button_font = pygame.font.Font(font_path,  int(25*vh_factor))
        btn_size = 280 * vh_factor
        btn_spacing = 20 * vh_factor

        start_pos = Vector2(vw/2 - (3*btn_size + 2*btn_spacing)/2,
                            vh/2 - (2*btn_size + 1*btn_spacing)/2)
        
        self.popup:dict[str, UIButton | UIImage] = {}
        self.buttons_list:list[UIButton] = list()
        self.buttons_list.append(button_back) # On ajoute aussi le bouton de retour

        # Lvl0
        button_lvl0 = UIButton(start_pos.x + 0*(btn_size+btn_spacing), start_pos.y, btn_size, btn_size, "NIVEAU 1", self.button_font, font_color=(177, 208, 207), color_idle=btn_normal_image, color_hover=btn_hover_image)
        button_lvl0.set_callback(callback=partial(button_callback_level_generic, 0))
        self.ui_manager.add_element(button_lvl0)
        self.buttons_list.append(button_lvl0)

        # Lvl1
        button_lvl1 = UIButton(start_pos.x + 1*(btn_size+btn_spacing), start_pos.y, btn_size, btn_size, "NIVEAU 2", self.button_font, font_color=(177, 208, 207), color_idle=btn_normal_image, color_hover=btn_hover_image)
        button_lvl1.set_callback(callback=partial(button_callback_level_generic, 1))
        self.ui_manager.add_element(button_lvl1)
        self.buttons_list.append(button_lvl1)

        # Lvl2
        button_lvl2 = UIButton(start_pos.x + 2*(btn_size+btn_spacing), start_pos.y, btn_size, btn_size, "NIVEAU 3", self.button_font, font_color=(177, 208, 207), color_idle=btn_normal_image, color_hover=btn_hover_image)
        button_lvl2.set_callback(callback=partial(button_callback_level_generic, 2))
        self.ui_manager.add_element(button_lvl2)
        self.buttons_list.append(button_lvl2)

        # Lvl3
        button_lvl3 = UIButton(start_pos.x + 0*(btn_size+btn_spacing), start_pos.y + (btn_size+btn_spacing), btn_size, btn_size, "NIVEAU 4", self.button_font, font_color=(177, 208, 207), color_idle=btn_normal_image, color_hover=btn_hover_image)
        button_lvl3.set_callback(callback=partial(button_callback_level_generic, 3))
        self.ui_manager.add_element(button_lvl3)
        self.buttons_list.append(button_lvl3)

        # Lvl4
        button_lvl4 = UIButton(start_pos.x + 1*(btn_size+btn_spacing), start_pos.y + (btn_size+btn_spacing), btn_size, btn_size, "NIVEAU 5", self.button_font, font_color=(177, 208, 207), color_idle=btn_normal_image, color_hover=btn_hover_image)
        button_lvl4.set_callback(callback=partial(button_callback_level_generic, 4))
        self.ui_manager.add_element(button_lvl4)
        self.buttons_list.append(button_lvl4)

        # Lvl5
        button_lvl5 = UIButton(start_pos.x + 2*(btn_size+btn_spacing), start_pos.y + (btn_size+btn_spacing), btn_size, btn_size, "NIVEAU 6", self.button_font, font_color=(177, 208, 207), color_idle=btn_normal_image, color_hover=btn_hover_image)
        button_lvl5.set_callback(callback=partial(button_callback_level_generic, 5))
        self.ui_manager.add_element(button_lvl5)
        self.buttons_list.append(button_lvl5)

    def load_level(self, level_id):
        self.game.change_scene(scene_name="Loading", reload_scene=True, scene_arguments={"lvl":level_id})

    def create_popup(self, level_id:int):
        if self.popup or not (0 <= level_id <= 5):
            return # Évite d'ouvrir plusieurs popups ou un popup invalide
                
        images = {
            0: path.join(base_path, "data", "img", "fiches", "monalisa.png"),
            1: path.join(base_path, "data", "img", "fiches", "thedream.png"),
            2: path.join(base_path, "data", "img", "fiches", "thestarrynight.png"),
            3: path.join(base_path, "data", "img", "fiches", "thescream.png"),
            4: path.join(base_path, "data", "img", "fiches", "kanagawa.png"),
            5: path.join(base_path, "data", "img", "fiches", "warrior.png")
        }
    
        bg_image = images.get(level_id)
        if not bg_image:
            return # Aucun popup si l’image n’existe pas
        
        popup_size = Vector2(self.game.vh, self.game.vh) * 0.9
        popup_pos = Vector2(self.game.vw/2 - popup_size.x/2, self.game.vh*0.05)

        self.popup["background"] = UIImage(
            popup_pos.x, popup_pos.y, popup_size.x, popup_size.y, image_path=bg_image
        )

        offset = 10
        self.popup["close_btn"] = UIButton(
            popup_pos.x-offset, popup_pos.y-offset, 30, 30, 
            text="X", 
            font_color=(0,0,0),
            font=pygame.font.Font(None, 20), 
            color_idle=(240, 186, 57), 
            color_hover=(220, 166, 47)
        )
        self.popup["close_btn"].set_callback(self.close_popup)

        self.popup["play_btn"] = UIButton(
            self.game.vw/2 - popup_size.x/4, popup_pos.y + popup_size.y*0.83, popup_size.x/2, 70,
            text="Jouer",
            font=self.button_font,
            font_color=(255,255,255),
            color_idle=(240, 186, 57), 
            color_hover=(200, 146, 37),
            borde_width=max(1, int(10*self.game.vh/1000))
        )
        self.popup["play_btn"].set_callback(partial(self.load_level, level_id))

        # Ajout des éléments à l'UI
        for element in self.popup.values():
            self.ui_manager.add_element(element)

        # Désactivation des boutons de sélection
        for btn in self.buttons_list:
            btn.interactive = False
    
    def close_popup(self):
        if not self.popup:
            return

        # Réactivation des boutons de sélection
        for btn in self.buttons_list:
            btn.interactive = True

        # Suppression des éléments du popup de l'UI
        for element in self.popup.values():
            self.ui_manager.remove_element(element)

        self.popup.clear()
        del self.popup
        self.popup = {}

        
    def update(self, dt):
        super().update(dt)

        self.mouse_pos = self.mouse_pos*0.95*(1-dt) + Vector2(self.mouse_x, self.mouse_y)*0.05

    def draw(self, screen):
        screen.fill(self.bg_color)
        screen.blit(self.bg_image, self.bg_image.get_rect(topleft=(-0.5*self.game.vh - ease_in_out(self.mouse_pos.x, 1.5)*PARALLAX_INTENSITY, -PARALLAX_INTENSITY -ease_in_out(self.mouse_pos.y, 1.5)*PARALLAX_INTENSITY))) # image background

        super().draw(screen)

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pygame.MOUSEMOTION:
            self.mouse_x = (event.pos[0]*2 / self.game.vw - 1)
            self.mouse_y = (event.pos[1]*2 / self.game.vh - 1)