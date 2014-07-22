from itertools import chain
import pygame as pg
from .. import tools, prepare

class BuildingPlacement(tools._State):
    def __init__(self):    
        super(BuildingPlacement, self).__init__()
        self.next = "MANAGING"
        self.index = (0, 0)
        
    def startup(self, persistent):
        self.persist = persistent
        self.player = persistent["player"]
        self.building_type = persistent["building type"]
        self.world = persistent["world"]
        self.footprint = self.building_type.footprint
        self.build_size = self.building_type.size

    def update(self, surface, keys):
        mouse_pos = pg.mouse.get_pos()
        self.world.scroll(mouse_pos)
        
        for cell in self.world.grid:
            if self.world.grid[cell].rect.collidepoint(mouse_pos):
                self.index = cell
                break
        
        self.tl_index = (self.index[0], self.index[1] - (int(self.build_size[1]/16)))      
        self.placement_valid = True
        try:
            self.build_rect = pg.Rect((self.world.grid[self.tl_index].rect.left,
                                             self.world.grid[self.tl_index].rect.top),
                                             self.build_size)
        except KeyError:
            self.placement_valid = False
        self.foot_rect = pg.Rect(0, 0, self.footprint[0] * 16, self.footprint[1] * 16)
        self.foot_rect.bottomleft = self.build_rect.bottomleft
        self.collision_rect = self.foot_rect.inflate(32, 32)
        cells = self.world.grid.values()
        if any([x.occupied for x in cells if x.rect.colliderect(self.collision_rect)]):
            self.placement_valid = False
        if any([e.rect.colliderect(self.collision_rect) for e in self.world.elves]):
            self.placement_valid = False
        
        
        self.draw(surface)
    
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.next = "MANAGING"
                self.done = True
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.placement_valid:
                    new_building = self.building_type(self.tl_index , self.world)
                    self.world.buildings = sorted(self.world.buildings, key=lambda x: x.rect.bottom)
                    self.world.decorations = sorted(self.world.decorations, key=lambda x:x.rect.bottom)
                else:
                    self.persist["message"] = "This structure cannot be placed here"
                    self.persist["previous"] = "BUILDINGPLACEMENT"
                    self.next = "MESSAGEWINDOW"
                    self.done = True
            else:
                self.next = "MANAGING"
                self.done = True
                
    def draw(self, surface):    
        surface.fill(pg.Color("white"))
        self.world.draw(surface)
        
        place_color = (0, 255, 0, 50) if self.placement_valid else (255, 0, 0, 50)
        alpha_surf = pg.Surface(self.build_rect.size).convert_alpha()
        alpha_surf.fill(place_color)
        surface.blit(alpha_surf, self.build_rect) 
        
        