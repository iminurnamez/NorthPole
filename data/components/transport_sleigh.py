from itertools import cycle
import pygame as pg
from .. import prepare


class TransportSleigh(object):
    front_reins = prepare.GFX["reins"]
    back_reins = prepare.GFX["backreins"]
    sleigh_image = prepare.GFX["sleigh"]
    
    def __init__(self, lefttop, airport):
        self.port = airport
        left_deer1 = pg.transform.flip(prepare.GFX["rightreindeer1"], True, False)
        left_deer2 =  pg.transform.flip(prepare.GFX["rightreindeer2"], True, False)
        self.reindeer_images = cycle([left_deer1, left_deer2])
        self.reindeer_image = next(self.reindeer_images)
        self.surface = pg.Surface(self.sleigh_image.get_size())
        self.surface.set_colorkey(pg.Color("black"))
        self.rect = self.surface.get_rect(topleft=lefttop)
        self.direction = -1
        self.speed = 1
        self.ticks = 0
        self.flying_ticks = 0
        self.loading_ticks = 0
        self.state = "Loading"
        self.state_updates = {"Takeoff": self.takeoff,
                                         "Departing": self.depart,
                                         "Flying": self.fly,
                                         "Arriving": self.arrive,
                                         "Loading": self.load_sleigh}
        
    
    def takeoff(self, world):
        if self.rect.right < self.port.landing_spot.left:
                self.rect.move_ip(self.direction * self.speed, 0)
        else:        
            self.state = "Departing"
            
    def depart(self, world):
        if self.rect.left > world.grid[(world.tiles_wide - 1, 0)].rect.left:
            self.state = "Flying"
            self.flying_ticks = 1000            
        elif self.rect.top > self.port.rect.top - 100:
            self.rect.move_ip(self.direction * self.speed, -1)
        else:
            self.rect.move_ip(self.direction * self.speed, 0)
            
        
    def fly(self, world):
        self.flying_ticks -= 1
        if self.flying_ticks <= 0:
            self.state = "Arriving"
            self.direction = -1
            self.rect.left = world.grid[(world.tiles_wide - 1, 0)].rect.left + 200
            self.rect.top = self.port.rect.top - 200
            
    def arrive(self, world):
        spot = self.port.landing_spot
        if self.rect.left < self.port.arrive_rect.left:
            self.state = "Loading"
            self.loading_ticks = 500
        elif self.rect.left > spot.left + (200 * self.speed):
            self.rect.move_ip(self.direction * self.speed, 0)
        elif self.rect.top < spot.top:
            self.rect.move_ip(self.direction * self.speed, 1)
        else:
            self.rect.move_ip(self.direction * self.speed, 0)
            
    def load_sleigh(self, world):
        self.loading_ticks -= 1
        if self.loading_ticks <= 0:
            self.state = "Takeoff"
            self.direction = 1
            self.rect.topleft = self.port.arrive_rect.topleft
            
    def move(self, offset):
        self.rect.move_ip(offset)    
            
    def update(self, world):
        self.ticks += 1
        self.state_updates[self.state](world)
        if not self.ticks % 6:
            self.reindeer_image = next(self.reindeer_images)       
        
    def draw(self, surface):
        if self.state != "Loading":
            self.surface.fill(pg.Color("black"))
            for tl in [(0, 12), (22, 12), (44, 12), (66, 12)]:
                self.surface.blit(self.reindeer_image, tl)
            self.surface.blit(self.back_reins, (9, 10))
            self.surface.blit(self.sleigh_image, (0, 0))
            for _tl in [(0, 16), (22, 16), (44, 16), (66, 16)]:
                self.surface.blit(self.reindeer_image, _tl)
            self.surface.blit(self.front_reins, (9, 14))
            if self.direction == 1:
                self.surface = pg.transform.flip(self.surface, True, False)
            surface.blit(self.surface, self.rect)
                               
        