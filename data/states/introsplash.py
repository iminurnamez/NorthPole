import pygame as pg

from .. import tools, prepare
from ..components import transport_sleigh

class IntroSplash(tools._State):
    def __init__(self):
        super(IntroSplash, self).__init__()
        self.next = "INSTRUCTIONSPLASH"
        self.player = prepare.PLAYER
        self.image = prepare.GFX["title"]
        center_point = pg.display.get_surface().get_rect().center
        self.image_rect = self.image.get_rect(center=center_point)
        self.cursor = prepare.GFX["canecursor"]
        screen = pg.display.get_surface().get_rect()
        self.sleigh = transport_sleigh.TransportSleigh((screen.right + 10, 200), None)
        self.persist["player"] = self.player
        pg.mouse.set_visible(False)
        
    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            self.done = True
            
    def update(self, surface, keys):
        surface.blit(self.image, self.image_rect)
        self.sleigh.rect.move_ip(-1, 0)
        self.sleigh.draw(surface)
        surface.blit(self.cursor, pg.mouse.get_pos()) 

