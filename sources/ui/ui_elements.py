#Projet : Tetr'Art
#Auteurs : Andrea CARATTI, Mohamad KARANOUH, Issam MOUTAWAKKIL, Raphael BRICAUD, Ulysse LEONARD SCHWARZ

import pygame
from pygame import Vector2

class UIElement:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = True  # Permet de masquer l'élément
        self.interactive = True  # Permet de désactiver les interactions avec l'élément
        
    def draw(self, screen):
        pass
    
    def handle_event(self, event):
        if not self.interactive:
            return

class Label(UIElement):
    def __init__(self, x, y, text, font:pygame.font.Font, color=(255, 255, 255), text_align="L-C-R"):
        super().__init__(x, y, 0, 0)

        self.position = Vector2(x,y)
        self.text = text
        self.font = font
        self.color = color
        self.text_align = text_align if text_align != "L-C-R" else "L"
        text_surface = self.font.render(self.text, True, self.color)
        self.rect = text_surface.get_rect(topleft=(x, y))
        self.text_surface = text_surface


    def draw(self, screen, reset=False):
        if not self.visible:
            return
        topleft = list(self.rect.topleft)
        if self.text_align == "C":
            topleft[0] -= self.rect.width/2
        elif self.text_align == "R":
            topleft[0] -= self.rect.width
        screen.blit(self.text_surface, topleft)
    
    def set_text(self, text:str):
        self.text = text
        text_surface = self.font.render(text, True, self.color)
        self.rect = text_surface.get_rect(topleft=(self.position.x, self.position.y))
        self.text_surface = text_surface


class UIImage(UIElement):
    def __init__(self, x, y, width, height, image_path):
        super().__init__(x, y, 0, 0)
        self.image = pygame.image.load(image_path)
        if width and height:
            self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.visible = True

    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, self.rect.topleft)

    def set_position(self, x, y):
        self.rect.topleft = (x, y)

    def resize(self, width, height):
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=self.rect.topleft)
    
    def handle_event(self, event):
        pass


class Frame(UIElement):
    def __init__(self, x, y, width, height, background_color=(0, 0, 0), padding=10, border_size=0, border_color=(0,0,0)):
        super().__init__(x, y, width, height)

        self.background_color = background_color
        self.padding = padding

        self.border_size = border_size
        self.border_color = border_color

        self.elements = []

    def add_element(self, element):
        '''
        Ajoute un élément à la frame.
        '''
        self.elements.append(element)

    def draw(self, screen):
        if not self.visible:
            return
        
        if len(self.background_color) == 3:
            pygame.draw.rect(screen, self.background_color, self.rect)
        elif len(self.background_color) == 4:
            transparent_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            transparent_surface.fill(self.background_color)
            screen.blit(transparent_surface, (self.rect.x, self.rect.y))

        if self.border_size > 0:
            pygame.draw.rect(screen, self.border_color, self.rect, max(1, int(self.border_size)))

        for element in self.elements:
            if isinstance(element, UIElement):
                element.rect.topleft = (self.rect.x + self.padding, self.rect.y + self.padding)
                element.draw(screen)

    def handle_event(self, event):
        super().handle_event(event)
        for element in self.elements:
            if isinstance(element, UIElement):
                element.handle_event(event)


class VerticalLayout:
    def __init__(self, x, y, padding=10):
        '''
        Ne pas utilisé, ne fonctionne pas correctement
        '''
        super().__init__(x, y, 0, 0)

        self.x = x
        self.y = y
        self.padding = padding
        self.elements = []

    def add_element(self, element):
        self.elements.append(element)
        self.arrange()

    def arrange(self):
        current_y = self.y
        for element in self.elements:
            element.rect.topleft = (self.x, current_y)
            current_y += element.rect.height + self.padding

    def draw(self, screen):
        for element in self.elements:
            element.draw(screen)

    def handle_event(self, event):
        super().handle_event(event)
        for element in self.elements:
            element.handle_event(event)


class UIButton(UIElement):
    def __init__(self, x, y, width, height, text, font, color_idle=None, color_hover=None, color_pressed=None, font_color=(255,255,255), borde_width=0):
        super().__init__(x, y, width, height)

        self.text = text
        self.font = font
        self.color_idle = color_idle
        self.color_hover = color_hover or self.color_idle
        self.color_pressed = color_pressed or self.color_hover
        self.current_color = color_idle
        self.font_color = font_color
        self.background_enabled = (color_idle != None)
        self.borde_width = borde_width or 0
        self.is_pressed = False
        self.callback = None

    def draw(self, screen):
        
        if not self.visible:
            return
        if self.background_enabled:
            if isinstance(self.current_color, tuple) and len(self.current_color)==3:
                pygame.draw.rect(screen, self.current_color, self.rect, border_radius=5, width=self.borde_width)
            elif isinstance(self.current_color, pygame.surface.Surface):
                self.current_color = pygame.transform.scale(self.current_color, self.rect.size)
                screen.blit(self.current_color, self.rect)
        text_surface = self.font.render(self.text, True, self.font_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        super().handle_event(event)

        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.current_color = self.color_hover
            else:
                self.current_color = self.color_idle

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.current_color = self.color_pressed
                self.is_pressed = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.is_pressed:
                self.is_pressed = False
            if self.rect.collidepoint(event.pos) and self.callback:
                    self.callback()
            self.current_color = self.color_hover if self.rect.collidepoint(event.pos) else self.color_idle

    def set_callback(self, callback):
        self.callback = callback

class SliderValue():
    def __init__(self, value: float):
        '''
        Float between 0 and 1
        '''
        self._value = max(0, min(value, 1))

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = max(0, min(new_value, 1))

class UIThumb():
    def __init__(self, radius, color_idle=None, color_hover=None):
        self.color_idle = color_idle or (255,255,255)
        self.color_hover = color_hover or color_idle
        self.current_color = color_idle
        self.radius = radius
        self.rect:pygame.rect.Rect = pygame.Rect(0, 0, 2 * radius, 2 * radius)

    def draw(self, screen, x, y):
        self.rect = pygame.rect.Rect(x - self.radius, 
                                     y - self.radius, 
                                     2 * self.radius, 
                                     2 * self.radius)
        pygame.draw.rect(screen,
                         self.current_color,
                         self.rect,
                         border_radius = self.radius)

    def handle_event(self, event):
        if self.rect:
            if event.type == pygame.MOUSEMOTION:
                if self.rect.collidepoint(event.pos):
                    self.current_color = self.color_hover
                else:
                    self.current_color = self.color_idle

        

class UISlider(UIElement):
    def __init__(self, x, y, width, height, color, thumb:UIThumb, value:SliderValue):
        super().__init__(x, y, width, height)
        self.thumb: UIThumb = thumb
        self.value: SliderValue = value
        self.color = color

        self.drag = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect,)

        thumb_x = self.rect.x + self.value.value * self.rect.width
        thumb_y =  self.rect.y + self.rect.height/2

        self.thumb.draw(screen, thumb_x, thumb_y)

    def handle_event(self, event):
        super().handle_event(event)

        self.thumb.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.thumb.rect and self.thumb.rect.collidepoint(event.pos):
                    self.drag = True

        elif event.type == pygame.MOUSEBUTTONUP:
                self.drag = False

        elif event.type == pygame.MOUSEMOTION and self.drag:
            new_value = (event.pos[0] - self.rect.x) / self.rect.width
            self.value.value = new_value