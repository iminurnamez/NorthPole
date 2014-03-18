import pygame as pg

from .. import tools, prepare

class InstructionSplash(tools._State):
    def __init__(self):
        super(InstructionSplash, self).__init__()
        self.next = "MANAGING"
        self.image = prepare.GFX["instructions"]
        center_point = pg.display.get_surface().get_rect().center
        self.image_rect = self.image.get_rect(center=center_point)
        
        
    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            self.done = True
            
    def update(self, surface, keys):
        surface.blit(self.image, self.image_rect)
        
    def startup(self, persistant):
        self.player = persistant["player"]
        return tools._State.startup(self, persistant)
        
    def cleanup(self):
        self.persist["player"] = self.player
        self.done = False
        return tools._State.cleanup(self)