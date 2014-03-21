import itertools as it
import random
import pygame as pg
from .. import prepare
            
class Decoration(object):
    def __init__(self, name, index, world, size, tile_map):
        self.name = name
        self.index = index
        self.rect = pg.Rect(world.grid[self.index].rect.topleft, size)
        self.tile_map = tile_map
        column = len(self.tile_map[0]) - 1
        row = 0
        for line in self.tile_map:
            for char in line[::-1]:
                index = (self.index[0] + column,
                              self.index[1] + row)
                if char != "X":
                    world.grid[index].occupied = True
                
                column -= 1
            row += 1
            column = len(self.tile_map[0]) - 1
       
    def move(self, offset):
        self.rect.move_ip(offset)
        self.cheer_rect.move_ip(offset)
            
    def display(self, surface):
        surface.blit(self.image, self.rect)
    
    def update(self, world):
        for elf in [x for x in world.elves if x.state in {"Travelling",
                                                                           "Hauling"}]:
            if elf.rect.colliderect(self.cheer_rect):
                elf.cheer += self.cheer_quality
                if elf.cheer > elf.max_cheer:
                    elf.cheer = elf.max_cheer

class XmasTree(Decoration):
    def __init__(self, index, world):                
        tile_map = ["XX",
                          "TX"]
        super(XmasTree, self).__init__("Xmas Tree", index, world,
                                                      (32, 32), tile_map)     
        self.image = prepare.GFX["xmastree"]
        self.light_cycle = it.cycle([prepare.GFX["treelights" + str(x)] for
                                               x in range(1, 5)])         
        self.lights = next(self.light_cycle)
        self.lights_rect = self.lights.get_rect(topleft=(self.rect.left,
                                                              self.rect.top + 9))
        self.cheer_rect = pg.Rect(self.rect.left - 16, self.rect.top, 48, 48)
        self.cheer_quality = .1
        
    def move(self):
        self.rect.move_ip(offset)
        self.cheer_rect.move_ip(offset)
        self.lights_rect.move_ip(offset)
        
    def display(self, surface):
        surface.blit(self.image, self.rect)
        surface.blit(self.lights, self.lights_rect)
        
    def update(self, world):
        elves = world.elves
        for elf in [x for x in elves if x.state in {"Travelling",
                                                                           "Hauling"}]:
            if elf.rect.colliderect(self.cheer_rect):
                elf.cheer += self.cheer_quality
                if elf.cheer > elf.max_cheer:
                    elf.cheer = elf.max_cheer
        if not world.ticks % 10:
            self.lights = next(self.light_cycle)
            
            
class WavySanta(Decoration):
    def __init__(self, index, world):
        tile_map = ["XX",
                          "XX",
                          "XX",
                          "SS"]
        super(WavySanta, self).__init__("Wavy Santa", index, world, (32, 64), tile_map)
        self.images = it.cycle([prepare.GFX["wavy1"], prepare.GFX["wavy2"]])
        self.image = next(self.images)        
        self.cheer_rect = pg.Rect(self.rect.left - 48, self.rect.top, 128, 128)
        self.cheer_quality = .15        
    
    def update(self, world):
        elves = world.elves
        for elf in [x for x in elves if x.state in {"Travelling",
                                                                           "Hauling"}]:
            if elf.rect.colliderect(self.cheer_rect):
                elf.cheer += self.cheer_quality
                if elf.cheer > elf.max_cheer:
                    elf.cheer = elf.max_cheer
        if not world.ticks % 5:
            self.image = next(self.images)

            
class PyroBox(Decoration):
    colors = [
                  #"dodgerblue4",
                  #"orangered",
                  #"green2",
                  #"cyan",
                  #"red3",
                  #"darkorchid",
                  #"aquamarine3",
                  "darkgreen",
                  "forestgreen",
                  "red4",
                  "slategray1",
                  "darkgoldenrod",
                  "red2"
                  #"maroon1"
                  #"lightseagreen"
                  #"mediumorchid3"
                  ]
    def __init__(self, index, world):                
        tile_map = ["XX",
                          "BX"]
        super(PyroBox, self).__init__("Fireworks", index, world, (32, 32),
                                                    tile_map)     
        self.image = prepare.GFX["pyrobox"]
        self.cheer_rect = pg.Rect(0, 0, 320, 320)
        self.cheer_rect.center = self.rect.center
        self.ticks = 1
        self.fireworks = []
        self.cheer_quality = .35
        
    def move(self):
        self.rect.move_ip(offset)

        
    def display(self, surface):
        surface.blit(self.image, self.rect)
        for firework in self.fireworks:
            firework.display(surface)
        
        
    def update(self, world):
        if not world.ticks % 500:
            self.firing = True
            self.delay = 1
            points = [(3, 16), (3, 21), (8, 16), (8, 21), (13, 16), (13, 21)]             
            for point in points:
                color = random.choice(self.colors)
                center_point = (self.rect.left + point[0],
                                        self.rect.top + point[1])
                x_velocity = random.uniform(-.4, .4)
                y_velocity = random.uniform(-1.0, -2.0)
                altitude = center_point[1] - random.randint(120, 200)
                delay = random.randint(5, 150)
                self.fireworks.append(Firework(color, center_point, x_velocity,
                                                              y_velocity, altitude, delay, self))
                
        if self.fireworks:
            for elf in [x for x in world.elves if x.state in {"Travelling",
                                                                               "Hauling"}]:
                if elf.rect.colliderect(self.cheer_rect):
                    elf.cheer += self.cheer_quality
                    if elf.cheer > elf.max_cheer:
                        elf.cheer = elf.max_cheer
            for firework in self.fireworks:
                firework.update(world)
        else:
            self.firing = False
        self.ticks += 1
    
   
class Firework(object):
    def __init__(self, color, center_point, x_velocity, y_velocity, altitude,
                         delay, pyro_box):
        self.start_y = center_point[0]
        self.x_pos = center_point[0]
        self.y_pos = center_point[1]
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.color = color 
        self.rocket_rect = pg.Rect(0, 0, 2, 2)
        self.rocket_rect.center = center_point
        if random.choice((True, False, False)):
            self.images = iter([prepare.GFX["{}firework_ring{}".format(self.color, i)] for
                                       i in range(1, 15)])
        else:
            self.images = iter([prepare.GFX["{}firework{}".format(self.color, i)] for
                                       i in range(1, 15)])        
        self.altitude = altitude
        self.delay = delay
        self.pyro_box = pyro_box
        self.exploded = False
        self.done = False
        
        
    def display(self, surface):
        if self.delay > 0:
            return
        if not self.exploded: 
            if not self.covered:        
                pg.draw.rect(surface, pg.Color(self.color), self.rocket_rect)
        else:
            surface.blit(self.image, self.rect)            
            
    def update(self, world):
        self.delay -= 1
        if self.done:
            self.pyro_box.fireworks.remove(self)
        if self.delay > 0:
            return
        if not self.exploded:
            self.covered = False
            for item in [x for x in it.chain(world.trees, world.buildings,
                              world.decorations) if x.rect.bottom < self.start_y]:
                if item.rect.collidepoint(self.x_pos, self.y_pos):
                    self.covered = True
                    break
        
            if self.y_pos <= self.altitude:
                self.exploded = True
                self.image = next(self.images)
                self.rect = self.image.get_rect(center = self.rocket_rect.center)
                self.ticks = 1
            else:
                self.x_pos += self.x_velocity
                self.y_pos += self.y_velocity
                self.rocket_rect.center = (int(self.x_pos), int(self.y_pos))
        else:    
            try:
                if not self.ticks % 6:
                    self.image = next(self.images)
            except StopIteration:
                self.done = True
            self.ticks += 1
