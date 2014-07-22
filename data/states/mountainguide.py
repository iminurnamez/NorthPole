import os
import pygame as pg

from .. import prepare, tools


class MountainGuide(tools._State):
    def __init__(self):
        super(MountainGuide, self).__init__()
        self.next = "BOARDING"
        self.image = prepare.GFX["mtkringleguide"]
        center_point = pg.display.get_surface().get_rect().center
        self.image_rect = self.image.get_rect(center=center_point)
        self.cursor = prepare.GFX["canecursor"]
    
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            self.done = True
            
    def update(self, surface, keys):
        surface.fill(pg.Color("white"))
        surface.blit(self.image, self.image_rect)
        surface.blit(self.cursor, pg.mouse.get_pos())
        
    def startup(self, persistant):
        pg.mouse.set_visible(False)
        pg.mixer.music.fadeout(1500)
        self.__init__()
        self.player = persistant["player"] 
        return tools._State.startup(self, persistant)
        
    def cleanup(self):
        self.persist["player"] = self.player
        self.done = False
        return tools._State.cleanup(self)