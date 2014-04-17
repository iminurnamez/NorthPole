from math import radians, sin, cos, hypot
from random import uniform
import pygame as pg

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
        if self.power < 30:
            self.loft -= 1.5
        elif self.power < 60:
            self.loft -= 1
        elif self.power < 85:
            self.loft -= .5
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
        self.rattled = False
        
               
    @property
    def int_pos(self):
        return (int(self.pos[0]), int(self.pos[1]))
    
    def move(self):
        vx = self.speed * cos(self.angle) * uniform(.3, 1.6)
        vy = self.speed * sin(self.angle) * uniform(.3, 1.6)
        self.pos = (self.pos[0] + vx, self.pos[1] - vy)
        
    
    def update(self, hole):
        screen_rect = pg.display.get_surface().get_rect()
        obstacles = hole.obstacles
        int_pos = self.int_pos
        
        if not self.landed:
            if self.altitude > self.loft + self.initial_height:
                self.peaked = True
            if self.altitude < 1:
                self.landed = True
                       
            for item in obstacles:
                if item.disc_collider.collidepoint(int_pos):
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
            old_pos = self.pos
            self.move()
            if not screen_rect.collidepoint(self.pos):
                print "Out of Bounds"
                self.pos = old_pos
                
    def draw(self, surface):
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
        super(Cupid, self).__init__(5, 4, .05, .15, "deeppink", pos, power, angle)       
        
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
        super(Blitzen, self).__init__(12.5, 4, .1, .3, "blue", pos, power, angle)
        
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