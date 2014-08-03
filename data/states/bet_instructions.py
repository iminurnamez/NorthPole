import pygame as pg

from .. import tools, prepare

class BettingSplash(tools._State):
    def __init__(self):
        super(BettingSplash, self).__init__()
        self.next = "BETTING"
        self.image = prepare.GFX["betinstruct"]
        center_point = pg.display.get_surface().get_rect().center
        self.image_rect = self.image.get_rect(center=center_point)
        self.cursor = prepare.GFX["canecursor"]
        
    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            self.done = True
        
    def update(self, surface, keys, dt):
        surface.blit(self.image, self.image_rect)
        surface.blit(self.cursor, pg.mouse.get_pos())