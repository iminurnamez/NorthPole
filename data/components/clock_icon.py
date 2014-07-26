from math import pi, cos, sin
import pygame as pg
from .. import prepare, tools


class ClockIcon(object):
    def __init__(self, center_point):
        self.center = center_point
        self.image = prepare.GFX["clockicon"]
        self.rect = self.image.get_rect(center=center_point)
        self.radius = self.rect.width / 2.0
        self.speed = .002
        self.minute_terminus = 0.0
        self.hour_terminus = 0.0
        self.minute_angle = 0.0
        self.hour_angle = 0.0
        self.plus = prepare.GFX["plussign"]
        self.minus = prepare.GFX["minussign"]
        self.plus_rect = self.plus.get_rect(midleft=(self.rect.right + 10, self.rect.centery))
        self.minus_rect = self.minus.get_rect(midright=(self.rect.left - 10, self.rect.centery))
        
    def update(self):
        self.hour_angle -= self.speed
        self.minute_angle -= self.speed * 12.0
        self.hour_angle = self.hour_angle % (2 * pi)
        self.minute_angle = self.minute_angle % (2 * pi)
        self.minute_terminus = (self.center[0] + (cos(self.minute_angle) * (self.radius * .8)),
                                             self.center[1] - (sin(self.minute_angle) * (self.radius * .8)))
        self.hour_terminus = (self.center[0] + (cos(self.hour_angle) * (self.radius * .6)),
                                         self.center[1] - (sin(self.hour_angle) * (self.radius * .6)))
                                         
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        pg.draw.line(surface, pg.Color("gray1"), self.center, self.hour_terminus)
        pg.draw.line(surface, pg.Color("gray1"), self.center, self.minute_terminus)
        surface.blit(self.plus, self.plus_rect)
        surface.blit(self.minus, self.minus_rect)
        