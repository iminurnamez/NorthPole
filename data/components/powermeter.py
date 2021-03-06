import pygame as pg


class PowerMeter(object):
    def __init__(self, middletop, callback=None):
        self.surface = pg.Surface((100, 10))
        self.rect = self.surface.get_rect(midtop=middletop)
        self.level = 0
        self.action = None
        self.callback = callback
       
    def fill_meter(self):
        self.level += max(1.5, self.level / 20)
        if self.level >= 100.0:
            self.level = 100.0
            self.action = self.drain_meter
 
    def drain_meter(self):
        self.level -= 1.5
        if self.level <= 0.0:
            self.level = 0.0
            self.action = None
 
    def interrupt(self):
        if self.action is None:
            if self.level > 0:
                self.level = 0.0
            else:
                self.action = self.fill_meter
        else:
            self.action = None
            if self.callback is not None:
                self.callback()

         
    def update(self):
        if self.action is not None:
            self.action()
 
    def draw(self, surface):
        self.surface.fill(pg.Color("gray1"))
        bar = pg.Rect((0, 0), (int(self.level), 10))
        bar_color = (int(255 - (self.level * 2.5)), int(2.5 * self.level), 0)                                  
        pg.draw.rect(self.surface, bar_color, bar)
        pg.draw.rect(self.surface, pg.Color("lightgray"), self.surface.get_rect(), 2)
        surface.blit(self.surface, self.rect)
        