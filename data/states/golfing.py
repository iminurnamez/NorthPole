from __future__ import print_function

import sys
import os
from random import uniform, randint
from math import sin, cos, radians, hypot
import itertools as it
import pygame as pg
from .. import tools, prepare
from ..components.obstacles import Tree, DiscBasket, TeeBox
from ..components import discs, golfer, golfhole
from ..components.powermeter import PowerMeter
                                                  
class Golfing(tools._State):
    def __init__(self):
        super(Golfing, self).__init__()
        self.done = False
        self.next = "MANAGING"
        self.fps = 60        
       
    def startup(self, persistant):   
        self.screen_rect = pg.display.get_surface().get_rect()
        hole_items = prepare.DGCOURSE[persistant["hole"]]
        self.hole = golfhole.DiscGolfHole(hole_items)
        self.player = persistant["player"]
        self.golfer = golfer.Golfer(self.hole.teebox.rect.center)
        self.power_meter = PowerMeter((self.screen_rect.centerx - 50,
                                                         self.screen_rect.height - 20),
                                                         self.add_disc)        
  
    def cleanup(self):
        self.persist["player"] = self.player
        self.done = False
        return tools._State.cleanup(self)
        
    def get_event(self, event):        
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.next = "MANAGING"
                self.done = True
            elif event.key == pg.K_d:
                self.golfer.next_disc()
            elif event.key == pg.K_SPACE:
                self.power_meter.interrupt()
                       
    def add_disc(self):
        if not self.hole.disc:
            self.hole.disc = self.golfer.current_disc(self.golfer.rect.center,
                                                                      self.power_meter.level,
                                                                      self.golfer.angle)
        
    def update(self, surface, keys):
        if keys[pg.K_LEFT]:
            self.golfer.angle += 1
        elif keys[pg.K_RIGHT]:
            self.golfer.angle -= 1
        self.power_meter.update()
        self.hole.update()
        
        d = self.hole.disc
        if d:
            if d.landed:
                self.golfer.rect.center = d.int_pos
                self.hole.disc = None
            elif self.hole.basket.disc_collider.collidepoint(d.int_pos):
                print("Chains rattled")
                prepare.SFX["chain"].play()
                pg.time.delay(1500)
                self.done = True 
                # TODO add score
        
        self.draw(surface)
       
    def draw(self, surface):
        surface.fill(pg.Color("white"))
        self.hole.draw(surface)
        self.golfer.draw(surface)
        self.power_meter.draw(surface)
        surface.blit(self.golfer.info_label.text, (0, surface.get_height() - 20))
        
    
    