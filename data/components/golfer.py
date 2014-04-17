from math import radians, sin, cos
import itertools as it
import pygame as pg
from labels import TransparentLabel
from discs import (Rudolph, Cupid, Donder, Vixen, Dasher,
                              Prancer, Blitzen, Dancer, Comet)


class Golfer(object):
    def __init__(self, centerpoint):
        self.rect = pg.Rect(0, 0, 4, 4)
        self.rect.center = centerpoint
        self.angle = 90
        self.discs = it.cycle([Rudolph, Cupid, Donder, Vixen, Dasher,
                                       Prancer, Blitzen, Dancer, Comet])
        self.current_disc = next(self.discs)
        info = "DISC: {} - {}".format(self.current_disc.name, self.current_disc.tagline)
        self.info_label = TransparentLabel(10, info, "gray1", "topleft", 0, 0, "white")
    
    def next_disc(self):
        self.current_disc = next(self.discs)
        info = "DISC: {} - {}".format(self.current_disc.name, self.current_disc.tagline)
        self.info_label = TransparentLabel(10, info, "gray1", "topleft", 0, 0, "white")

    def update(self):
        pass
            
    def draw(self, surface):
        pg.draw.rect(surface, pg.Color("blue"), self.rect)
        r_angle = radians(self.angle)
        center = self.rect.center
        pg.draw.line(surface, pg.Color("black"), center,
                           (int(center[0] + (50 * cos(r_angle))),
                            int(center[1] - (50 * sin(r_angle)))))
              
            