from itertools import chain
import pygame as pg
from .. import tools, prepare

class BuildingPlacement(tools._State):
    def __init__(self):    
        super(BuildingPlacement, self).__init__()
        self.next = "MANAGING"
        self.index = (0, 0)
        
    def startup(self, persistant):
        self.player = persistant["player"]
        self.building_type = persistant["building type"]
        self.world = persistant["world"]
        self.footprint = self.building_type.footprint
        self.build_size = self.building_type.size

    def update(self, surface, keys):
        mouse_pos = pg.mouse.get_pos()
        for cell in self.world.grid:
            if self.world.grid[cell].rect.collidepoint(mouse_pos):
                self.index = cell
                break
        
        self.tl_index = (self.index[0], self.index[1] - (int(self.build_size[1]/16)))      
        
        try:
            self.build_rect = pg.Rect((self.world.grid[self.tl_index].rect.left,
                                             self.world.grid[self.tl_index].rect.top),
                                             self.build_size)
        except KeyError:
            pass
        self.foot_rect = pg.Rect(0, 0, self.footprint[0] * 16, self.footprint[1] * 16)
        self.foot_rect.bottomleft = self.build_rect.bottomleft
        self.collision_rect = self.foot_rect.inflate(32, 32)
        cells = self.world.grid.values()
        if any([x.occupied for x in cells if x.rect.colliderect(self.collision_rect)]):
            self.placement_valid = False
        else:
            self.placement_valid = True
        self.display(surface)
    
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.done = True
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.placement_valid:
                    print "Placed"
                    new_building = self.building_type(self.tl_index , self.world)
                    self.world.buildings = sorted(self.world.buildings, key=lambda x: x.rect.bottom)
    def cleanup(self):
        self.persist["player"] = self.player
        self.done = False
        return self.persist
        
    def display(self, surface):    
        surface.fill(pg.Color("white"))
        self.world.display(surface)
        
        place_color = (0, 255, 0, 50) if self.placement_valid else (255, 0, 0, 50)
        alpha_surf = pg.Surface(self.build_rect.size).convert_alpha()
        alpha_surf.fill(place_color)
        surface.blit(alpha_surf, self.build_rect) 
        
        