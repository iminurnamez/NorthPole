import pygame as pg
from .. import prepare
from ..components.buildings import Building, SchoolTile, Window


class School(Building):
    footprint = (3, 3)
    size = (48, 96)
    name = "Schoolhouse"
    modes = ["Farming","Logging","Mining","Hauling","Husbandry",
                   "Baking","Woodworking","Metalworking","Stitchery"]
    def __init__(self, index, world):
        tile_map = ["XXX",
                          "XXX",
                          "XXX",
                          "OOO",
                          "OOO", 
                          "SXO"]
        char_map = {"S": SchoolTile}
        super(School, self).__init__(index, (1,5), world,
                                                  self.size, tile_map, char_map)
        self.exit = (self.entrance[0], self.entrance[1] + 1)
        self.windows = [Window((self.rect.left + 9, self.rect.top + 77), (5, 14)),
                                Window((self.rect.left + 34, self.rect.top + 77), (5, 14))]
        self.dimmer = pg.Surface((5, 14)).convert_alpha()
        self.dimmer.fill((0, 0, 0, 60))
        self.max_workers = 6

        
    def update(self, world):
        for window in self.windows:
            window.update(world)

        
        for elf in self.workers:
            elf.skills[self.mode] += .00001


                
    def draw(self, surface):
        for window in self.windows:
            window.draw(surface, len(self.workers))
            surface.blit(self.dimmer, window.rect)
        for tile in self.tiles:
            tile.draw(surface)
        
            
        