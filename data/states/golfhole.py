from __future__ import print_function

import sys
import os
from random import uniform, randint
from math import sin, cos, radians, hypot
import itertools as it
import pygame as pg


class PowerMeter(object):
    def __init__(self, lefttop):
        self.rect = pg.Rect(lefttop, (100, 10)) 
        self.surface = pg.Surface(self.rect.size)
        self.level = 0
        self.filling = False
        self.draining = False
        self.paused = False
        
    def pause(self):
        self.filling = False
        self.draining = False
        self.paused = True
    
    def reset(self):
        self.paused = False
        self.draining = False
        self.filling = False
        self.level = 0

    def update(self):
        if self.filling:
            self.level += max((1, self.level / 20))
            if self.level >= 100:
                self.level = 100
                self.filling = False
                self.draining = True
                
        elif self.draining:
            self.level -= 1.5
            if self.level < 0:
                self.level = 0
                self.draining = False
    
    def display(self, surface):
        self.surface.fill(pg.Color("gray1"))
        bar = pg.Rect((0, 0), (int(self.level), 10))
        bar_color = (int(255 - (self.level * 2.5)), int(2.5 * self.level), 0)                                  
        pg.draw.rect(self.surface, bar_color, bar)
        pg.draw.rect(self.surface, pg.Color("lightgray"), self.surface.get_rect(), 2)
        surface.blit(self.surface, self.rect)

        
class Tree(object):
    def __init__(self, lefttop):
        self.rect = pg.Rect(lefttop, (5, 32))
        self.height = 7

        
class Disc(object):
    def __init__(self, speed, loft, pull, fade, color, pos, power, angle):
        self.base_speed = speed * .1
        self.loft = loft
        self.pull = pull
        self.fade = fade
        self.color = color
        self.initial_pos = pos
        self.pos = pos
        self.power = power
        self.speed = self.base_speed * self.power * .01
        self.angle = radians(angle)
        self.pull_angle = self.angle - (self.pull * 1.5)
        self.fade_angle = self.angle + (self.fade * 1.5)
        self.initial_height = 4
        self.altitude = 4
        self.radius = 4
        self.broke = False
        self.peaked = False
        self.landed = False
        self.collided = False
        
               
    @property
    def int_pos(self):
        return (int(self.pos[0]), int(self.pos[1]))
    
    def move(self):
        vx = self.speed * cos(self.angle) * uniform(.3, 1.6)
        vy = self.speed * sin(self.angle) * uniform(.3, 1.6)
        self.pos = (self.pos[0] + vx, self.pos[1] - vy)
        
    
    def update(self, basket, obstacles):
        obstacles = obstacles
        int_pos = self.int_pos
        
        if not self.landed:
            if self.altitude > self.loft + self.initial_height:
                self.peaked = True
            if self.altitude < 1:
                self.landed = True
                       
            for item in obstacles:
                if item.rect.collidepoint(int_pos):
                    if self.altitude <= item.height:
                        obj_dist = hypot(item.rect.centerx - self.initial_pos[0],
                                                          item.rect.centery - self.initial_pos[1])
                        disc_dist = hypot(int_pos[0] - self.initial_pos[0],
                                                          int_pos[1] - self.initial_pos[1])
                        if obj_dist > disc_dist:
                            self.collided = True
                            self.speed = self.base_speed * self.power * .004
                            self.angle = -self.angle
                            break
                     
            if not self.collided:
                if self.angle < self.pull_angle:
                    self.broke = True
                if self.broke and self.angle < self.fade_angle:
                    self.angle += .03 * self.fade
                else:
                    self.angle -= .01 * self.pull
                if self.peaked:
                    self.altitude -= .02
                else:
                    self.altitude += .0325        
            else:
                self.altitude -= .025
            self.move()
            
            if basket.rect.collidepoint(self.int_pos):
                print("Chains rattled")  
            
    def display(self, surface, trailing):
        pg.draw.circle(surface, pg.Color(self.color),
                              self.int_pos, max((int(self.altitude), 4)))


class Rudolph(Disc):
    name = "Rudolph"
    tagline = "This putter guides the way straight to the chains"
    def __init__(self, pos, power, angle):
        super(Rudolph, self).__init__(6, 1, 0, .1, "red",  pos, power, angle)
        
class Cupid(Disc):
    name = "Cupid"
    tagline = "A long approach disc with good loft" 
    def __init__(self, pos, power, angle):
        super(Cupid, self).__init__(6.5, 4, .05, .15, "deeppink", pos, power, angle)       
        
class Donder(Disc):
    name = "Donder"
    tagline = "A basic mid-range disc"
    def __init__(self, pos, power, angle):
        super(Donder, self).__init__(9, 3, .1, .2, "lightblue",  pos, power, angle)

class Vixen(Disc):
    name = "Vixen"
    tagline = "A mid-range disc with wicked curves"
    def __init__(self, pos, power, angle):
        super(Vixen, self).__init__(9, 3, .45, .6, "maroon",  pos, power, angle)
        
class Dasher(Disc):
    name = "Dasher"
    tagline = "A fairway driver with minimal movement"
    def __init__(self, pos, power, angle):
        super(Dasher, self).__init__(10, 3.5, .1, .2, "green",  pos, power, angle)
        
class Prancer(Disc):
    name = "Prancer"
    tagline = "A fairway driver with good loft and moderate movement"
    def __init__(self, pos, power, angle):
        super(Prancer, self).__init__(10, 4, .3, .3, "orange",  pos, power, angle)
        
class Blitzen(Disc):
    name  = "Blitzen"
    tagline = "A driver that finishes left"
    def __init__(self, pos, power, angle):
        super(Blitzen, self).__init__(12.5, 4, .2, .3, "blue", pos, power, angle)
        
class Dancer(Disc):
    name = "Dancer"
    tagline = "A driver with lots of movement"
    def __init__(self, pos, power, angle):
        super(Dancer, self).__init__(11.5, 4, .35, .35, "purple",  pos, power, angle)
        
class Comet(Disc):
    name = "Comet"
    tagline = "A stellar distance driver"
    def __init__(self, pos, power, angle):
        super(Comet, self).__init__(13, 4, .025, .1, "yellow",  pos, power, angle)

                                                  
class DiscGolfHole(tools._State):
    def __init__(self):
        super(DiscGolfHole, self).__init__()
        self.done = False
        self.next = "DGSCORECARD"
        self.fps = 60        
       
    def startup(self, persistant):   
        self.disc_types = it.cycle([Rudolph, Cupid, Donder, Vixen, Dasher,
                                              Prancer, Blitzen, Dancer, Comet])
        self.disc_type = next(self.disc_types)
        self.disc = None
        self.player = persistant["player"]
        self.player.rect = pg.Rect(0, 0, 10, 10) 
        self.player
        self.player_angle = 90
        self.trees = [Tree((randint(10, 1070),
                           randint(10, 730))) for _ in range(30)]
        
        #self.basket = pg.image.load("discbasket.png").convert()
        #self.basket.set_colorkey(pg.Color("black"))
        self.basket_rect = pg.Rect((randint(100, 700), randint(50, 450)), (5, 30))
        self.marker = pg.Rect(self.basket_rect.left, self.basket_rect.top + 5, 5, 8)
        
        info = "DISC: {} - {}".format(self.disc_type.name, self.disc_type.tagline)
        self.info_label = self.font.render(info, True, pg.Color("white"), pg.Color("black"))
        self.power_meter = PowerMeter((self.player_rect.centerx - 50,
                                                         self.screen.get_height() - 20,
                                                         self.add_disc()))        
         
    def add_disc(self):
        self.discs.append(self.disc_type(self.player_rect.center,
                                  self.power_meter.level, self.player_angle))
                                  
    def next_disc(self):
        self.disc_type = next(self.disc_types)
        info = "DISC: {} - {}".format(self.disc_type.name, self.disc_type.tagline)
        self.info_label = self.font.render(info, True, pg.Color("white"), pg.Color("black"))
    
    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.done = True
                elif event.key == pg.K_d:
                    self.next_disc()
                elif event.key == pg.K_f:
                    if self.fullscreen:
                        pg.display.set_mode(self.screen_size)    
                        self.fullscreen = False
                    else:                
                        pg.display.set_mode(self.screen_size, pg.FULLSCREEN)
                        self.fullscreen = True
                                            
                elif event.key == pg.K_t:
                    self.trailing = not self.trailing
                elif event.key == pg.K_SPACE:
                    self.power_meter.interrupt()
                    
                   
        keys = pg.key.get_pressed()        
        if keys[pg.K_LEFT]:
            self.player_angle += 1
        elif keys[pg.K_RIGHT]:
            self.player_angle -= 1
                       
    def update(self):
        self.power_meter.update()
        for disc in self.discs:
            disc.update(self.basket_rect, self.trees)
        
    def draw(self):    
        self.screen.fill(pg.Color("black"))
        for tree in self.trees:
            pg.draw.rect(self.screen, pg.Color("darkgreen"), tree)
        #self.screen.blit(self.basket, self.basket_rect)
        pg.draw.rect(self.screen, pg.Color("lightgray"), self.basket_rect)
        pg.draw.rect(self.screen, pg.Color("orange"), self.marker)
        for disc in self.discs:
            disc.display(self.screen, self.trailing)
        r_angle = radians(self.player_angle)
        center = self.player_rect.center
        pg.draw.line(self.screen, pg.Color("white"), center,
                           (int(center[0] + (50 * cos(r_angle))),
                            int(center[1] - (50 * sin(r_angle)))))
        self.screen.blit(self.info_label, (0, self.screen.get_height() - 20))
        self.power_meter.display(self.screen)

    def run(self):
        while not self.done:
            self.event_loop()
            self.update()
            self.draw()
            pg.display.update()
            self.clock.tick(self.fps)
        
if __name__ == "__main__":
    game = DiscGolf(1080, 740, 60)
    game.run()
    pg.quit()
    sys.exit()