import pygame as pg

from .. import prepare

                   
import pygame as pg

LOADED_FONTS = {}
                   
class _Label(object):
    '''Parent class all labels inherit from. Color arguments can use color names
       or an RGB tuple. rect_attributes should be a dict with keys of
       pygame.Rect attribute names (strings) and the relevant position(s) as values.'''
    def __init__(self, font_path, font_size, text, text_color, rect_attributes,
                         bground_color=None):
        if (font_path, font_size) not in LOADED_FONTS:
            LOADED_FONTS[(font_path, font_size)] = pg.font.Font(font_path,
                                                                                             font_size)
        f = LOADED_FONTS[(font_path, font_size)]    
        if bground_color is not None:
            self.text = f.render(text, True, pg.Color(text_color),
                                         pg.Color(bground_color))
        else:
            self.text = f.render(text, True, pg.Color(text_color))
        
        self.rect = self.text.get_rect(**rect_attributes)

    def draw(self, surface):
        surface.blit(self.text, self.rect)


class Label(_Label):
    '''Creates a surface with text blitted to it (self.text) and an associated
       rectangle (self.rect). Label will have a transparent background if
       bground_color is not passed to __init__.'''
    def __init__(self, font_path, font_size, text, text_color, rect_attributes,
                         bground_color=None):
        super(Label, self).__init__(font_path, font_size, text, text_color,
                                                rect_attributes, bground_color)

       
class GroupLabel(Label):                             
    '''Creates a Label object which is then appended to group.'''
    def __init__(self, group, font_path, font_size, text, text_color,
                         rect_attributes, bground_color=None):
        super(GroupLabel, self).__init__(font_path, font_size, text, text_color,
                                                        rect_attributes, bground_color)
        group.append(self)


class Button(object):
    def __init__(self, left, top, width, height, label):
        self.rect = pg.Rect(left, top, width, height)
        label.rect.center = self.rect.center
        self.label = label
       
        
    def draw(self, surface):
       pg.draw.rect(surface, pg.Color("white"), self.rect)
       pg.draw.rect(surface, pg.Color("maroon"), self.rect, 2)
       self.label.draw(surface)
       

class GroupButton(Button):
    def __init__(self, group, left, top, width, height, label, payload, amount):
        super(GroupButton, self).__init__(left, top, width, height, label, payload, amount)
        group.append(self)


class PayloadButton(Button):
    def __init__(self, left, top, width, height, label, payload):
        super(PayloadButton, self).__init__(left, top, width, height, label)
        self.payload = payload
        

class Meter(object):
    def __init__(self, midleft, width, height, value):
        self.frame = pg.Rect(midleft[0], midleft[1] - height/2, width, height)
        self.bar = pg.Rect(self.frame.left, self.frame.top, int(width * value), height)
        val = max(0, min(255, int(value * 255)))
        self.color = (255 - val, val, 0)
    
    def draw(self, surface):
        pg.draw.rect(surface, pg.Color("gray20"), self.frame)
        pg.draw.rect(surface, self.color, self.bar)
        pg.draw.rect(surface, pg.Color("gray40"), self.frame, 2)

        
