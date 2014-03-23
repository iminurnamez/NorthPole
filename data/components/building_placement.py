from itertools import chain
import pygame as pg
from .. import tools, prepare

class BuildingPlacement(tools._State):
    def __init__(self,     
        self.next = "MANAGING"
        self.index = (0, 0)
        
    def startup(self, persistant):
        self.player = persistant["player"]
        self.building_type = persistant["building type"]
        self.world = persistant["world"]
        self.footprint = self.building_type.footprint
        self.elves = self.world.elves
        self.buildings = self.world.buildings
        
        
    def update(self, surface, keys):
        mouse_pos = pg.mouse.get_pos()
        for cell in self.world.grid:
            if cell.rect.collidepoint(mouse_pos):
                self.index = cell.index
                break
        self.tl_index = (self.index[0], self.footprint[1]        
        self.build_rect = pg.Rect(self.world[self.index].rect.left,
                                             self.world[self.index].rect.top - (
                                             16 * (self.footprint[1] - 1)),
                                             (self.footprint[0] * 16, 
                                             self.footprint[1] * 16))
        self.collision_rect = self.build_rect.inflate(32, 32)
        
        for item in chain(self.buildings, self.elves):
            if item.rect.colliderect(self.build_rect):
                self.placement_invalid = 1
                break
        else:
            self.placement_invalid = 0
    
    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if not self.placement_invalid:
                    self.world.buildings.append(self.building_type(
                    
        
    def display(self, surface):    
        self.world.display(surface)
        place_color = (255 * self.placement_invalid, 255 * self.placement_invalid, 0, 50)
        pg.draw.rect(surface, place_color, self.build_rect) 
        
        