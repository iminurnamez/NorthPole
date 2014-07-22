import pygame as pg
from .. import prepare
from ..components.buildings import Building, DentistOfficeTile, Window

class DentistOffice(Building):
    footprint = (4, 3)
    size = (64, 64)
    name = "Dentist's Office"
    def __init__(self, index, world):
        tile_map = ["XXXX",
                          "OOOO",
                          "OOOO", 
                          "DOXO"]
        char_map = {"D": DentistOfficeTile}
        super(DentistOffice, self).__init__(index, (2, 3), world,
                                                      self.size, tile_map, char_map)
        self.exit = (self.entrance[0], self.entrance[1] + 1)
        self.windows = [Window((self.rect.left + 8, self.rect.top + 43), (20, 14))]
        self.dimmer = pg.Surface((20, 14)).convert_alpha()
        self.dimmer.fill((0, 0, 0, 60))
        self.max_workers = 1
        self.max_patrons = 1
        self.drilling = 0
        self.dental1 = prepare.GFX["dental1"]
        self.dental2 = prepare.GFX["dental2"]
        self.dental_empty = prepare.GFX["dentalempty"]
        self.dental_img = self.dental_empty
        world.dental_buildings.append(self)
        
    def update(self, world):
        for window in self.windows:
            window.update(world)
        self.drilling = max(0, self.drilling -1)
        if self.workers and self.patrons:
            for elf in self.patrons:
                elf.cavities += .05 # TODO - should be elf skill
            if not world.ticks % 100:
                self.drilling = 30
            if self.drilling:
                self.dental_img = self.dental2
            else:
                self.dental_img = self.dental1
        else:
            self.dental_img = self.dental_empty        
    
    def draw(self, surface):
        for window in self.windows:
            window.draw(surface, len(self.workers))
            surface.blit(self.dimmer, window.rect)
        for tile in self.tiles:
            tile.draw(surface)
        surface.blit(self.dental_img, (self.rect.left + 8, self.rect.top + 43))
            
        