from itertools import cycle
import pygame as pg
from .. import prepare
from .buildings import Building

class Sawmill(Building):
    footprint = (7, 6)
    size = (128, 112)
    name = "Sawmill"
    
    def __init__(self, index, world):
        tile_map = ["XXXXXXXX",
                          "OOOOOOOX",
                          "OOOOOOOX",
                          "OOOOOOOX",
                          "OOOOOOOX",
                          "OOOOOOOX",
                          "OOOXOOOX"]
        char_map = {}        
        super(Sawmill, self).__init__(index, (3, 6), world, self.size,
                                                   tile_map, char_map)
        self.inputs = {"Wood": 0.0}
        self.outputs = {"Lumber": 0.0}
        self.floor = prepare.GFX["sawmillfloor"]
        self.table = prepare.GFX["sawtable"]
        saw = prepare.GFX["sawblade"]
        self.saws = cycle([saw, pg.transform.flip(saw, False, True)])
        self.saw = next(self.saws)
        self.log = prepare.GFX["log"]
        self.log_rect = self.log.get_rect(topleft=(78, 78))
        self.roof = prepare.GFX["sawmillshell"]
        self.surface = pg.Surface((112, 112)).convert()
        self.surface.set_colorkey(pg.Color("black"))
        self.max_workers = 3
        
    def update(self, world):
        if self.workers:
            if not world.ticks % 6:
                self.saw = next(self.saws)
            if self.inputs["Wood"] >= .02:    
                self.log_rect.move_ip(-1, 0)
                if self.log_rect.left < 25:
                    self.log_rect.left = 78
            for worker in self.workers:    
                if self.inputs["Wood"] >= .02:
                    self.inputs["Wood"] -= .02    
                    self.outputs["Lumber"] += .01
            
    def draw(self, surface):
        self.surface.fill(pg.Color("black"))
        #self.surface.blit(self.floor, (10, 68))
        self.surface.blit(self.table, (56, 78))
        self.surface.blit(self.saw, (78, 68))
        if self.workers and self.inputs["Wood"] >= .02:
            self.surface.blit(self.log, self.log_rect)
        self.surface.blit(self.roof, (0, 0))
        surface.blit(self.surface, self.rect)