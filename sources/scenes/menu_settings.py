#Projet : Tetr'Art
#Auteurs : Andrea CARATTI, Mohamad KARANOUH, Issam MOUTAWAKKIL, Raphael BRICAUD, Ulysse LEONARD SCHWARZ

from os import path
from engine.scenes import *
from config import base_path
from functools import partial

class BindButton():
    def __init__(x, y, width, height, text, font, color, key_name, index, Menu):
        pass

keyname_unicode = {
    "return" : "↲",
    "left" : "←",
    "right" : "→",
    "up" : "↑",
    "down" : "↓",
    "left ctrl" : "x",
    "left alt" : "⌥",
    "left meta" : "⌘",
    "left shift" : "⇧",
    "right ctrl" : "x",
    "right alt" : "⌥",
    "right meta" : "⌘",
    "right shift" : "⇧",
    "backspace" : "⌫",
    "caps lock" : "⇪",
    "tab" : "⇥",
    "escape" : "␛",
}

def get_unicode_from_keycode(keyname):
    new_keyname = keyname_unicode.get(keyname)
    if new_keyname:
        return new_keyname
    else:
        return str(keyname)

class Settings_Menu(Scene):
    def __init__(self, game):
        self.load(game, {})

    def load(self, game, scene_arguments):
        super().load(game, scene_arguments)
        self.bg_color = (50,50,50)

        self.inputs_btns: dict[str, list] = {} # Used to change the key's name on the button
        self.Bind_Key_Name = ""
        self.Bind_Key_Index = 0
        self.isBinding = False

        # Key Binging System
        
        def ask_Bind(Name, Index):
            if self.isBinding:
                return
            self.Bind_Key_Name = Name
            self.Bind_Key_Index = Index
            if self.inputs_btns[Name] and self.inputs_btns[Name][Index]:
                self.inputs_btns[Name][Index].text = "><"
            self.isBinding = True

        # Return Button
        def button_callback_back():
            self.game.change_scene("Menu", False)
        button_back = UIButton(300,720,200,50, "Retour", self.game.font, None)
        button_back.set_callback(button_callback_back)
        self.ui_manager.add_element(button_back)

        # Title 
        vh_fac = self.game.vh/1000
        font_path_1 = path.join(base_path,"data","fonts","ChakraPetch-Bold.ttf")
        font_h1 = pygame.font.Font(font_path_1, int(80 * vh_fac))

        title = Label(x=int(self.game.vw/2), y=int(60*vh_fac), text="OPTIONS", font=font_h1, color=(255,255,255), text_align="C")
        self.ui_manager.add_element(title)

        # Create key binding section
        self.create_key_bindings(ask_Bind)
        
    def create_key_bindings(self, ask_Bind):
        vh_fac = self.game.vh / 1000
        font_path_2 = path.join(base_path, "data", "fonts", "BaiJamjuree-Regular.ttf")
        font_path_3 = path.join(base_path, "data", "fonts", "NotoSansSymbols-Bold.ttf")
        font_text = pygame.font.Font(font_path_2, int(33 * vh_fac))
        font_btn = pygame.font.Font(font_path_3, int(33 * vh_fac))
        offset_y = int(280 * vh_fac)

        # for each KeyInput
        for _input in self.game.settings.inputs.values():
            # Input Name display
            input_label = Label(x=int(160*vh_fac), y=offset_y, text=_input.display, font=font_text, color=(255,255,255), text_align="L")
            self.ui_manager.add_element(input_label)

            offset_x = 0
            key_btns = list()
            # Key Binding
            for i, key in enumerate(_input.keys):
                key_btn_text = get_unicode_from_keycode(pygame.key.name(key)).capitalize()
                key_btn = UIButton(x=int(self.game.vw/2 + offset_x), y=offset_y, width=int(60*vh_fac), height=int(60*vh_fac), text=key_btn_text, font=font_btn, color_idle=(180,180,180), color_hover=(150,150,150))
                key_btn.set_callback(callback=partial(ask_Bind, _input.name, i))
                key_btns.append(key_btn)
                offset_x+=100
                self.ui_manager.add_element(key_btn)

            self.inputs_btns[_input.name] = key_btns

            offset_y+=int(60*vh_fac)


    def draw(self, screen):
        screen.fill(self.bg_color)
        super().draw(screen)

    def handle_event(self, event):
        if self.isBinding:
            if event.type == pygame.KEYDOWN:
                # Replace keycode
                if self.game.settings.inputs[self.Bind_Key_Name]:
                    self.game.settings.inputs[self.Bind_Key_Name].keys[self.Bind_Key_Index] = event.key

                # Replace key display
                if self.inputs_btns[self.Bind_Key_Name] and self.inputs_btns[self.Bind_Key_Name][self.Bind_Key_Index]:
                    self.inputs_btns[self.Bind_Key_Name][self.Bind_Key_Index].text = get_unicode_from_keycode(pygame.key.name(event.key)).capitalize() #pygame.key.name(event.key).capitalize()
                    print(pygame.key.name(event.key))
                self.isBinding = False
                return
        super().handle_event(event)