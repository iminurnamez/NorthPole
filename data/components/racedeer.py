import itertools as it
import pygame as pg

from .. import prepare

class RaceDeer(object):
    def __init__(self, center_point, name, num, color, speed, stamina):
        self.x_pos = center_point[0]
        self.y_pos = center_point[1]
        self.image_list = [prepare.GFX["racedeer1"]] * 5
        self.image_list.extend([prepare.GFX["racedeer2"],
                                           prepare.GFX["racedeer3"],
                                           prepare.GFX["racedeer2"]])
        self.images = it.cycle(self.image_list)
        self.image = next(self.images)
        self.rect = self.image.get_rect(center=center_point)
        self.surface = pg.Surface(self.rect.size)
        self.surface.set_colorkey(pg.Color("black"))
        self.surface.blit(self.image, (0, 0))
        self.name = name
        self.num = num
        self.color = color        
        self.speed = speed
        self.stamina = stamina
        self.energy = 100
        self.blanket_pos = (24, 24)
        
                
        