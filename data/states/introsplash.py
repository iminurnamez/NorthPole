import pygame as pg

from .. import tools, prepare

class IntroSplash(tools._State):
    def __init__(self):
        super(IntroSplash, self).__init__()
        self.next = "INSTRUCTIONSPLASH"
        self.player = prepare.PLAYER
        self.image = prepare.GFX["title"]
        center_point = pg.display.get_surface().get_rect().center
        self.image_rect = self.image.get_rect(center=center_point)
        
        
    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            self.done = True
            
    def update(self, surface, keys):
        pg.display.get_surface().blit(self.image, self.image_rect)
        
    def startup(self, persistant):
        return tools._State.startup(self, persistant)
        
    def cleanup(self):
        self.persist["player"] = self.player
        self.done = False
        return tools._State.cleanup(self)