from itertools import cycle
from random import randint
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
        self.images = cycle(self.image_list)
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
        
    def update(self, race):
        if randint(1, 100) > self.stamina:
            self.energy -= .02
        if self.energy < 1:
            self.energy = 1
        movement = (randint(1, 1500) + 
                             (self.speed * self.energy * .01)) / 200.0
        if not race.ticks % int((10 - int(movement))/2):
            self.image = next(self.images)
            self.surface.fill(pg.Color("black"))
            self.surface.blit(self.image, (0, 0))                    
        self.x_pos += movement
        self.rect.centerx = int(self.x_pos - race.dist_travelled) 
        if self.x_pos >= race.distance and self not in race.results:
            race.results.append(self)
            race.racers.remove(self)
                
        