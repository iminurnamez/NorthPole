import pygame as pg
from obstacles import Tree, Rock, DiscBasket, TeeBox, TeeBoxVert

class DiscGolfHole(object):
    def __init__(self, obstacle_list):
        screen_rect = pg.display.get_surface().get_rect()
        class_map = {"tree": Tree,
                             "rock": Rock,
                             "discbasket": DiscBasket,
                             "teebox": TeeBox,
                             "teeboxvert": TeeBoxVert}

        self.obstacles = []
        for item in obstacle_list:
            if item[0] == "Width":
                self.width = item[1]
            elif item[0] == "Length":
                self.length = item[1]
            else:
                obstacle = class_map[item[0].lower()]((item[1][0] - ((self.width/2) - (screen_rect.width / 2)), item[1][1]), self)
        self.blitters = sorted(self.obstacles + [self.basket, self.teebox], key= lambda x: x.rect.y)
        self.disc = None
    
    def update(self):
        if self.disc:
            self.disc.update(self)
       
    def draw(self, surface):
        for blitter in self.blitters:
            blitter.display(surface)
        if self.disc:
            self.disc.draw(surface)                
       

