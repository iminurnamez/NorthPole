from itertools import cycle
from collections import defaultdict
import pygame as pg
from .. import prepare
from buildings import Building, BuildingTile
from transport_sleigh import TransportSleigh

class RunwayLight(object):
    def __init__(self, lefttop, color):
        self.image = prepare.GFX["runwaylight" + color]
        self.rect = self.image.get_rect(topleft=lefttop)
        self.surf = pg.Surface(self.rect.size).convert()
        self.surf.set_colorkey(pg.Color("black"))
        self.surf.blit(self.image, (0, 0))
        self.on = False
        
    def toggle(self):
        self.on = not self.on
        if self.on:
            self.surf.set_alpha(255)
        else:
            self.surf.set_alpha(96)
        
        
    def move(self, offset):
        self.rect.move_ip(offset)
        
    def draw(self, surface):
        surface.blit(self.surf, self.rect)
        
class LandingStripTile(BuildingTile):
    def __init__(self, index, world):
        super(LandingStripTile, self).__init__(index, "Landing Strip",
                                                               "landingstrip", world)
        
class LandingStrip(Building):
    footprint = (23, 11)
    size = (368, 176)
    name = "Landing Strip"
    def __init__(self, index, world):
        tile_map =  ["XXXXXXXXXXXXXXXXXXXXXXX",
                          "OOOOOOXXXXXXXXXXXXXXXXX",
                          "OOOOOOXXXXXXXXXXXXXXXXX",
                          "OOOOOOXXXXXXXXXXXXXXXXX",
                          "OOOOOOXXXXXXXXXXXXXXXXX",
                          "OOOOOOOXXXXXXXXXXXXXXXX",
                          "OOOOOOXXXXXXXXXXXXXXXXX",
                          "XOOOOOOOOOOOOOOOOOOOOOO",
                          "OOOOOOOOOOOOOOOOOOOOOOO",
                          "OOOOOOOOOOOOOOOOOOOOOOO",
                          "LOOOOOOOOOOOOOOOOOOOOOO"]
        char_map = {"L": LandingStripTile}                  
        super(LandingStrip, self).__init__(index, (0, 7), world,
                                                          self.size, tile_map,
                                                          char_map)
        colors = cycle(["red", "green"]) 
        self.light_pairs = []
        left = 359
        top1 = 108
        top2 = 171
        for i in range(15):
            color = next(colors)
            self.light_pairs.append((RunwayLight((left - (i * 16), top1), color),
                                                RunwayLight((left - (i * 16), top2), color)))
        self.lights_cycle = cycle(self.light_pairs)
        self.current_pair = next(self.lights_cycle)
        for light in self.current_pair:
            light.toggle()
        self.ticks = 0
        
        self.outputs = defaultdict(int)
        self.surf = pg.Surface(self.rect.size).convert()
        self.surf.set_colorkey(pg.Color("black"))
        
        self.arrive_rect = pg.Rect(self.rect.left + 32, self.rect.top + 122, 10, 10)
        self.landing_spot = pg.Rect(self.rect.left + 340, self.arrive_rect.top, 10, 10)
        self.sleighs = [TransportSleigh(self.arrive_rect.topleft, self)]
            
    def update(self, world):
        self.ticks += 1
        if not self.ticks % 7:
            for light in self.current_pair:
                light.toggle()
            self.current_pair = next(self.lights_cycle)
            for light in self.current_pair:
                light.toggle()
        for sleigh in self.sleighs:
            sleigh.update(world)
        
    def draw(self, surface):
        self.surf.fill(pg.Color("black"))
        for tile in self.tiles:
            self.surf.blit(tile.image, (0, 0))
        
        for light in self.light_pairs:
            light[0].draw(self.surf)
            light[1].draw(self.surf)
        
        surface.blit(self.surf, self.rect)
        for sleigh in self.sleighs:
            sleigh.draw(surface)
        
    def move(self, offset):
        
        self.rect.move_ip(offset)
        self.arrive_rect.move_ip(offset)
        self.landing_spot.move_ip(offset)
        
        for tile in self.tiles:
            tile.rect.move_ip(offset)
        for sleigh in self.sleighs:
            sleigh.move(offset)
        