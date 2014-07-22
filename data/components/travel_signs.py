import pygame as pg
from .. import prepare
from ..components.labels import Label


class TravelSign(object):
    size = (128, 96)
    footprint = (1, 1)
    name = "Travel Sign"
    def __init__(self, index, world, location_name, font, font_size):
        self.index = index
        self.destination = location_name
        blank = prepare.GFX["blanksign"]
        size = blank.get_size()
        self.rect = pg.Rect(world.grid[self.index].rect.topleft, size)
        
        self.sign = pg.Surface(size)
        self.sign.fill(pg.Color("black"))
        self.sign.blit(blank, (0, 0))
        self.sign.set_colorkey(pg.Color("black"))
        self.label = Label(font, font_size, location_name, "gray1", 
                                  {"center": (self.rect.left + 60, self.rect.top + 26)})
        self.tile_map = ["XXXXXXXX",
                                "XXXSXXXX"]
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
        self.label.rect.move_ip(offset)
       
    
    def draw(self, surface):
        surface.blit(self.sign, self.rect)
        self.label.draw(surface)
        
        