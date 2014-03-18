import pygame as pg

from .. import prepare

font_map = {12: prepare.TEXT12, 
                    14: prepare.TEXT14,
                    16: prepare.TEXT16,
                    18: prepare.TEXT18,
                    20: prepare.TEXT20,
                    24: prepare.TEXT24,
                    32: prepare.TEXT32,
                    48: prepare.TEXT48,
                    64: prepare.TEXT64}
                   
class MasterLabel(object):
    def __init__(self, font_size, text, text_color, rect_attribute,
                          x, y, bground_color):
        self.text = font_map[font_size].render(
                                           text, True, pg.Color(text_color),
                                           pg.Color(bground_color)).convert()
        if rect_attribute == "topleft":
            self.rect = self.text.get_rect(topleft = (x, y))
        elif rect_attribute == "topright": 
            self.rect = self.text.get_rect(topright = (x, y))
        elif rect_attribute == "bottomleft": 
            self.rect = self.text.get_rect(bottomleft = (x, y))
        elif rect_attribute == "bottomright": 
            self.rect = self.text.get_rect(bottomright = (x, y))
        elif rect_attribute == "midtop":
            self.rect = self.text.get_rect(midtop = (x, y))
        elif rect_attribute == "midbottom": 
            self.rect = self.text.get_rect(midbottom = (x, y))
        elif rect_attribute == "center": 
            self.rect = self.text.get_rect(center = (x, y))
        elif rect_attribute == "midleft": 
            self.rect = self.text.get_rect(midleft = (x, y))
        elif rect_attribute == "midright": 
            self.rect = self.text.get_rect(midright = (x, y))

    def display(self, surface):
        surface.blit(self.text, self.rect)

class Label(MasterLabel):
    def __init__(self, font_size, text, text_color, rect_attribute,
                          x, y, bground_color="black"):
        super(Label, self).__init__(font_size, text, text_color, rect_attribute,
                          x, y, bground_color)

       
class GroupLabel(MasterLabel):                             
    def __init__(self, group, font_size, text, text_color, rect_attribute,
                          x, y, bground_color="black"):
        super(GroupLabel, self).__init__(font_size, text, text_color, rect_attribute,
                          x, y, bground_color)
        group.append(self)

        
class TransparentLabel(Label):
    def __init__(self, font_size, text, text_color, rect_attribute,
                          x, y, bground_color="black"):
        super(TransparentLabel, self).__init__(font_size, text, text_color, rect_attribute,
                          x, y, bground_color)
        self.surface = pg.Surface(self.rect.size)
        self.surface.set_colorkey(pg.Color(bground_color))
        self.surface.blit(self.text, (0, 0))

    def display(self, surface):
        surface.blit(self.surface, self.rect)


class TransparentGroupLabel(TransparentLabel):
    def __init__(self, group, font_size, text, text_color, rect_attribute,
                          x, y, bground_color="black"):
        super(TranspGroupLabel, self).__init__(font_size, text, text_color,
                                                               rect_attribute, x, y, bground_color)
        self.surface = pg.Surface(self.rect.size)
        self.surface.set_colorkey(pg.Color(bground_color))
        self.surface.blit(self.text, (0, 0))
        group.append(self)


class Button(object):
    def __init__(self, left, top, width, height, label):
        self.rect = pg.Rect(left, top, width, height)
        label.rect.center = self.rect.center
        self.label = label
    
    def is_clicked(self, point):
        return self.rect.collidepoint(point)
        
    def display(self, surface):
       pg.draw.rect(surface, pg.Color("lightgray"), self.rect)
       pg.draw.rect(surface, pg.Color("gray30"), self.rect, 2)
       self.label.display(surface)

class PayloadButton(Button):
    def __init__(self, left, top, width, height, label, payload):
        super(PayloadButton, self).__init__(left, top, width, height, label)
        self.payload = payload
        
class GroupButton(Button):
    def __init__(self, group, left, top, width, height, label):
        super(GroupButton, self).__init__(left, top, width, height, label)
        group.append(self)
        
class Meter(object):
    def __init__(self, midleft, width, height, value):
        self.frame = pg.Rect(midleft[0], midleft[1] - height/2, width, height)
        self.bar = pg.Rect(self.frame.left, self.frame.top, width * value, height)
        self.color = (int(255 - (value * 255)), int(value * 255), 0)
        print self.color
        
    def display(self, surface):
        pg.draw.rect(surface, pg.Color("gray20"), self.frame)
        pg.draw.rect(surface, self.color, self.bar)
        pg.draw.rect(surface, pg.Color("gray40"), self.frame, 2)

