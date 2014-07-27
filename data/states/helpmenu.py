import pygame as pg
from .. import tools, prepare
from ..components.labels import Label, Button, PayloadButton


class HelpMenu(tools._State):
    def __init__(self):
        super(HelpMenu, self).__init__()
        
        self.window = pg.Rect(0, 0, 400, 500)
        self.window.center = pg.display.get_surface().get_rect().center
        self.cursor = prepare.GFX["questionmark"]
        self.font = prepare.FONTS["weblysleekuil"]
        done_label = Label(self.font, 18, "DONE", "gray1", {"topleft": (0, 0)},
                                     "white")
        self.done_button = Button(self.window.centerx - 40,
                                                self.window.bottom - 60, 80, 50,
                                                done_label)
        self.buttons = []
        payloads = ["Elves", "Buildings", "Resources", "Controls"]
        top = self.window.top + 50
        for payload in payloads:
            label = Label(self.font, 24, payload, "gray1", {"center": (0, 0)})
            button = PayloadButton(self.window.centerx - 60,
                                                top, 120, 50, label, payload)
            self.buttons.append(button)
            top += button.rect.height + 20
        
        self.next_states = {"Elves": "ELFHELP",
                                     "Buildings": "BUILDINGTYPESELECTION",
                                     "Resources": "RESOURCEHELP",
                                     "Controls": "CONTROLSHELP"}    
                                                
    def startup(self, persistent):
        pg.mouse.set_visible(False)
        self.persist = persistent
        self.persist["helping"] = True
        print "HELPMENU"
        
                                     
        
            
    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.done_button.rect.collidepoint(event.pos):
                    self.next = "MANAGING"
                    self.persist["helping"] = False
                    self.done = True
                    return
                for button in self.buttons:
                    if button.rect.collidepoint(event.pos):
                        self.next = self.next_states[button.payload]
                        self.done = True
                        
            elif event.button == 3:
                self.next = "MANAGING"
                self.persist["helping"] = False
                self.done = True
                
    def update(self, surface, keys):
    
        self.draw(surface)
        
    def draw(self, surface):
        surface.fill(pg.Color("gray96"))
        self.persist["world"].draw(surface)
        pg.draw.rect(surface, pg.Color("white"), self.window)
        pg.draw.rect(surface, pg.Color("maroon"), self.window, 3)
        for button in self.buttons:
            button.draw(surface)
        self.done_button.draw(surface)
        surface.blit(self.cursor, pg.mouse.get_pos())
        
        