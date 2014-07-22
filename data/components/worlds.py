from random import randint
from collections import OrderedDict
import itertools as it
import pygame as pg
from .. import prepare
from ..components.travel_signs import TravelSign
from ..components.buildings import Tree, Ore

    
class Cell(object):
    def __init__(self, index, lefttop, width, height, tile=None):
        self.index = index
        self.rect = pg.Rect(lefttop, (width, height))
        self.tile = tile
        self.occupied = False
                
    def move(self, offset):
        self.rect.move_ip((offset[0], offset[1]))
        
    def get_open_neighbors(self, world):
        opens = {(self.index[0] - 1, self.index[1]), 
                      (self.index[0] + 1, self.index[1]), 
                      (self.index[0], self.index[1] - 1), 
                      (self.index[0], self.index[1] + 1)}
        grid = world.grid
        return [x for x in opens if x in grid and 
                    not grid[x].occupied]
        
class World(object):
    def __init__(self, width, height, tile_width, tile_height):
        self.width = width
        self.height = height        
        self.grid = {}
        left = 0
        top = 0
        self.tiles_wide = int(width / tile_width) 
        self.tiles_high = int(height / tile_height)
        for i in range(self.tiles_high):
            for j in range(self.tiles_wide):
                self.grid[(j, i)] = Cell((j, i), (left, top), tile_width, tile_height)
                left += tile_width
            left = 0
            top += tile_height
        self.background = pg.Surface((self.width, self.height))
        for cell in self.grid.values():
            self.background.blit(prepare.GFX["snow"], cell.rect)
            
        
        self.travel_signs = [TravelSign((self.tiles_wide/2, 0), self, "Mt. Kringle",
                                                      prepare.FONTS["weblysleekuili"], 12),
                                     TravelSign((0, self.tiles_high/2), self, "Mistletoe Downs",
                                                      prepare.FONTS["weblysleekuili"], 12),
                                     TravelSign((self.tiles_wide/2, self.tiles_high - 6), self, "Spruce Glen DGC",
                                                      prepare.FONTS["weblysleekuili"], 12),]      
        self.buildings = []
        self.ores = []
        for i in range(7):
            pos_index = (randint(0, self.tiles_wide - 2),
                                randint(0, self.tiles_high - 3)) 
            while True:
                check_rect = pg.Rect(self.grid[pos_index].rect.topleft, (16, 32))
                for r in [sign.rect for sign in it.chain(self.ores, self.travel_signs)]:
                    if r.colliderect(check_rect):
                        pos_index = (randint(0, self.tiles_wide -1),
                                            randint(0, self.tiles_high - 3))
                        break
                else:
                    ore = Ore(pos_index, self)
                    break
        
        self.trees = []
        for _ in range(200):
            _index = (randint(0, self.tiles_wide - 2),
                           randint(0, self.tiles_high - 3)) 
            ores = [x.rect.inflate(32, 32) for x in self.ores]
            signs = [x.rect for x in self.travel_signs]
            while True:
                _rect = pg.Rect(self.grid[_index].rect.topleft, (16, 32))
                trees = [x.rect for x in self.trees]
                for r in it.chain(ores, signs, trees):
                    if r.colliderect(_rect):
                        _index = (randint(0, self.tiles_wide -2),
                                       randint(0, self.tiles_high - 3))
                        break
                else:
                    tree = Tree(_index, self)
                    break

        
        
        self.rest_buildings = []
        self.cheer_buildings = []
        self.food_buildings = []
        self.dental_buildings = []
        self.decorations = []
        
        self.elves = []
        
        self.ticks = 1
        self.scroll_speed = 3
        
    def move(self, offset):
        for cell in self.grid:
            self.grid[cell].rect.move_ip(offset)
        for building in it.chain(self.buildings, self.decorations):
            building.move(offset)
        for elf in self.elves:
            elf.move(offset)
        for sign in self.travel_signs:
            sign.move(offset)
        for ore in self.ores:
            ore.move(offset)
            
    def scroll(self, mouse_pos):  
        screen = pg.display.get_surface().get_rect()
        scroll_margin = 25
        offsetx = 0
        offsety = 0
        mousex, mousey = mouse_pos
        extreme_left = self.grid[(0, 0)].rect.left
        extreme_right = self.grid[(self.tiles_wide - 1, 0)].rect.right
        extreme_top = self.grid[(0, 0)].rect.top
        extreme_bottom = self.grid[(0, self.tiles_high - 1)].rect.bottom
        if mousex < scroll_margin and  extreme_left < self.scroll_speed:
            offsetx = self.scroll_speed
        elif mousex > screen.right - scroll_margin and extreme_right > screen.right - self.scroll_speed :
            offsetx = -self.scroll_speed
        if mousey < scroll_margin and extreme_top < self.scroll_speed:
            offsety = self.scroll_speed
        elif mousey > screen.bottom - scroll_margin and extreme_bottom > screen.bottom - self.scroll_speed: 
            offsety = -self.scroll_speed
        if offsetx or offsety:
            self.move((offsetx, offsety))
            
    def update(self):
        for elf in self.elves:
            elf.update(self)
            elf.update_image(self)
            
        for building in it.chain(self.trees, self.buildings, self.decorations, self.ores):
            building.update(self)
        self.ticks += 1
        
    def draw(self, surface):
        surface.fill(pg.Color("grey96"))
        surface.blit(self.background, self.grid[(0,0)].rect.topleft)
        
            
        for elf in self.elves:
            elf.draw(surface)
        all_buildings = it.chain(self.buildings, self.ores, self.decorations)
        buildings = sorted(all_buildings, key=lambda x: x.rect.bottom)
        for building in buildings:
            building.draw(surface)
        for sign in self.travel_signs:
            sign.draw(surface)
        #for elf in self.elves:
        #    if elf.goal:
        #        pg.draw.rect(surface, pg.Color("blue"), self.grid[elf.goal].rect)
        #for cell in self.grid.values():    
        #    if cell.occupied:
        #        pg.draw.rect(surface, pg.Color("blue"), cell.rect)
            
            
        