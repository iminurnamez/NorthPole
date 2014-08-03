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
from ..components.labels import GroupLabel as GLabel
                                                  
class Golfing(tools._State):
    def __init__(self):
        super(Golfing, self).__init__()
        self.font = prepare.FONTS["weblysleekuil"]
        self.done = False
        self.next = "MANAGING"
        self.fps = 60
        self.showing_disc_info = True        
       
    def startup(self, persistant):   
        self.screen_rect = pg.display.get_surface().get_rect()        
        self.holes = iter([golfhole.DiscGolfHole(x) for x in prepare.DGCOURSE.values()])
        self.hole = next(self.holes)
        self.player = persistant["player"]
        self.golfer = golfer.Golfer(self.hole.teebox.rect.center)
        self.power_meter = PowerMeter((self.golfer.rect.centerx, self.golfer.rect.bottom + 30),
                                                       self.add_disc)
        self.update_disc_info(self.golfer.current_disc)                                                
        self.showing_disc_info = True
        
    def cleanup(self):
        self.persist["player"] = self.player
        self.done = False
        return tools._State.cleanup(self)
        
    def get_event(self, event):        
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.next = "MANAGING"
                self.done = True
            elif event.key == pg.K_UP:
                self.golfer.next_disc()
                self.update_disc_info(self.golfer.current_disc)
            elif event.key == pg.K_DOWN:
                #cycle through to previous disc
                for i in range(8):                # cycle object has no length
                    self.golfer.next_disc()
                self.update_disc_info(self.golfer.current_disc)
            elif event.key == pg.K_SPACE:
                self.power_meter.interrupt()
            elif event.key == pg.K_d:
                self.showing_disc_info = not self.showing_disc_info
                
    def add_disc(self):
        if not self.hole.disc:
            self.hole.disc = self.golfer.current_disc(self.golfer.rect.center,
                                                                      self.power_meter.level,
                                                                      self.golfer.angle)

    def update_disc_info(self, disc):
        self.labels = []
        converts = {"Rudolph": (5, 3, 0, 2),
                          "Cupid": (5, 10, 1, 2),
                          "Donder": (7, 7, 2, 3),
                          "Vixen": (7, 7, 8, 10),
                          "Dasher": (8, 9, 2, 3),
                          "Prancer": (8, 10, 5, 5),
                          "Blitzen": (10, 10, 2, 5),
                          "Dancer": (9, 10, 6, 6),
                          "Comet": (10, 10, 1, 2)}
        self.disc_ui_rect = pg.Rect(0, self.screen_rect.height - 150, 160, 150)
        dname = GLabel(self.labels, self.font, 14, disc.name, "darkgreen", {"midtop": ((self.disc_ui_rect.width - 60) / 2, self.disc_ui_rect.top + 10)}, "white")
        kind = GLabel(self.labels, self.font, 12, disc.kind, "maroon", {"midtop": (dname.rect.centerx, dname.rect.bottom + 5)}, "white")
        speed = GLabel(self.labels, self.font, 10, "Spd", "gray1", {"topleft": (5, kind.rect.bottom + 5)}, "white") 
        spd_num = GLabel(self.labels, self.font, 10, str(converts[disc.name][0]), "gray1", {"topright": (self.disc_ui_rect.left + 80, speed.rect.top)}, "white")
        loft = GLabel(self.labels, self.font, 10, "Loft", "gray1", {"topleft": (5, speed.rect.bottom + 5)}, "white")
        loft_num = GLabel(self.labels, self.font, 10, str(converts[disc.name][1]), "gray1", {"topright": (self.disc_ui_rect.left + 80, loft.rect.top)}, "white")
        pull = GLabel(self.labels, self.font, 10, "Draw", "gray1", {"topleft": (5, loft.rect.bottom + 5)}, "white")
        pull_num = GLabel(self.labels, self.font, 10, str(converts[disc.name][2]), "gray1", {"topright": (self.disc_ui_rect.left + 80, pull.rect.top)}, "white")
        fade = GLabel(self.labels, self.font, 10, "Fade", "gray1", {"topleft": (5, pull.rect.bottom + 5)}, "white")
        fade_num = GLabel(self.labels, self.font, 10, str(converts[disc.name][3]), "gray1", {"topright": (self.disc_ui_rect.left + 80, fade.rect.top)}, "white")
        self.disc_path = prepare.GFX[disc.name.lower()]
        
    def update(self, surface, keys, dt):
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
                self.power_meter.rect.midtop = (self.golfer.rect.centerx, self.golfer.rect.bottom + 50)
                self.hole.disc = None
            elif self.hole.basket.disc_collider.collidepoint(d.int_pos):
                prepare.SFX["chain"].play()
                pg.time.delay(1500)
                try:
                    self.hole = next(self.holes)
                    self.golfer.rect.center = self.hole.teebox.rect.center
                    self.power_meter.rect.midtop = (self.golfer.rect.centerx, self.golfer.rect.bottom + 50)
                except StopIteration:
                    self.done = True
                
                
                # TODO add score

        self.draw(surface)
       
    def draw(self, surface):
        surface.fill(pg.Color("white"))
        self.hole.draw(surface)
        self.golfer.draw(surface)
        self.power_meter.draw(surface)
        if self.showing_disc_info:
            pg.draw.rect(surface, pg.Color("white"), self.disc_ui_rect)
            surface.blit(self.disc_path, (self.disc_ui_rect.right - 60,
                                                     self.disc_ui_rect.top))
            pg.draw.rect(surface, pg.Color("maroon"), self.disc_ui_rect, 2) 
            for label in self.labels:
                label.draw(surface)


        
        
        #surface.blit(self.golfer.info_label.text, (0, surface.get_height() - 40))
        
    
