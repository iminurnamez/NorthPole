from collections import OrderedDict
import itertools as it
import pygame as pg
from .. import prepare

    
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
        self.grid = {}
        left = 0
        top = 0
        for i in range(height / tile_height):
            for j in range(width / tile_width):
                self.grid[(j, i)] = Cell((j, i), (left, top), tile_width, tile_height)
                left += tile_width
            left = 0
            top += tile_height
            
        self.trees = []
        self.elves = []
        self.buildings = []
        self.rest_buildings = []
        self.cheer_buildings = []
        self.food_buildings = []
        self.decorations = []
        self.ticks = 1
        
    def move(self, offset):
        for cell in self.grid:
            self.grid[cell].rect.move_ip(offset)
        for building in it.chain(self.trees, self.buildings, self.decorations):
            building.move(offset)
            
    def update(self):
        for elf in self.elves:
            elf.update(self)
            elf.update_image(self)
            
        for building in it.chain(self.trees, self.buildings, self.decorations):
            building.update(self)
        self.ticks += 1
        
    def display(self, surface):
        for elf in self.elves:
            elf.display(surface)
        for building in it.chain(self.trees, self.buildings, self.decorations):
            building.display(surface)
        #for elf in self.elves:
        #    if elf.goal:
        #        pg.draw.rect(surface, pg.Color("blue"), self.grid[elf.goal].rect)
            
            
            
            
        