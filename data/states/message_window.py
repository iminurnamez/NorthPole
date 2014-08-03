import pygame as pg
from .. import tools, prepare
from ..components.labels import Label, Button

class MessageWindow(tools._State):
    def __init__(self):
        super(MessageWindow, self).__init__()
        self.cursor = prepare.GFX["canecursor"]
        self.font = prepare.FONTS["weblysleekuil"]
        screen_rect = pg.display.get_surface().get_rect()
        self.window = pg.Rect(0, 0, 300, 100)
        self.window.center = screen_rect.center
    
    def startup(self, persistent): 
        self.persist = persistent
        self.next = self.persist["previous"]
        self.world = self.persist["world"]
        screen_rect = pg.display.get_surface().get_rect()
        self.labels = []
        self.msg_label = Label(self.font, 16, self.persist["message"],
                                    "gray1", 
                                    {"midtop": (self.window.centerx, self.window.top + 20)},
                                    "white")
        self.window = pg.Rect(0, 0, 300, 100)
        
        if self.msg_label.rect.width > 280:
            self.window = pg.Rect(0, 0, self.msg_label.rect.width + 20, 100)
        self.window.center = screen_rect.center
        self.msg_label.rect.midtop = (self.window.centerx, self.window.top + 20)
        ok = Label(self.font, 18, "OK", "darkgreen", {"center": (0, 0)}, "white")
        
        self.ok = Button(self.window.centerx - 30,
                                 self.window.bottom - 40, 60, 30, ok)                             
    
    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.ok.rect.collidepoint(event.pos):
                    self.done = True
            elif event.button == 3:
                self.done = True
                
    def update(self, surface, keys, dt):
        self.draw(surface)
        
    def draw(self, surface):
        self.world.draw(surface)
        pg.draw.rect(surface, pg.Color("white"), self.window)
        pg.draw.rect(surface, pg.Color("maroon"), self.window, 3)
        self.msg_label.draw(surface)
        self.ok.draw(surface)
        surface.blit(self.cursor, pg.mouse.get_pos())