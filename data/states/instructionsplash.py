import pygame as pg
from .. import tools, prepare
from ..components.labels import GroupLabel as GLabel

class InstructionSplash(tools._State):
    def __init__(self):
        super(InstructionSplash, self).__init__()
        self.next = "MANAGING"
        screen = pg.display.get_surface().get_rect()
        self.cursor = prepare.GFX["canecursor"]
        
        font = prepare.FONTS["weblysleekuil"]
        self.labels = []
        self.title = GLabel(self.labels, font, 48, "Controls", "maroon",
                                  {"midtop": (screen.centerx, screen.top + 10)})
        self.click = GLabel(self.labels, font, 32, "Click anywhere to continue", "maroon",
                                  {"midbottom": (screen.centerx, screen.bottom - 10)})
        instructs = ["Left-click to select",
                          "Right-click for construction menu",
                          "F to toggle fullscreen", 
                          "UP / Down  to change speed",
                          "ESC to exit"]
        top = self.title.rect.bottom + 20
        spacer = 20
        for inst in instructs:
            instruct = GLabel(self.labels, font, 24, inst, "darkgreen", 
                                      {"midtop": (screen.centerx, top)})
            top += instruct.rect.height + spacer
        
    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            self.done = True
            
    def update(self, surface, keys):
        surface.fill(pg.Color("white"))
        for label in self.labels:
            label.draw(surface)
        surface.blit(self.cursor, pg.mouse.get_pos())
        
    def startup(self, persistent):
        self.persist = persistent
        self.player = self.persist["player"]
        pg.mouse.set_visible(False)
        return tools._State.startup(self, persistent)
        