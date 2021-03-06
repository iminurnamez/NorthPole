import pygame as pg
from .. import tools, prepare
from ..components.labels import Label, Button, PayloadButton, Menu


class BuildingTypeSelection(tools._State):
    def __init__(self):
        self.cursor = prepare.GFX["hammercursor"] #["canecursor"]
        self.font = prepare.FONTS["weblysleekuil"]
        super(BuildingTypeSelection, self).__init__()
        screen_rect = pg.display.get_surface().get_rect()
        self.building_type = None
        self.menu = Menu((400, 500))
        menu = self.menu.rect
        self.title_label = Label(self.font, 24, "Select a building type", "darkgreen",
                                         {"midtop": (menu.centerx, menu.top + 10)},
                                         "white")
        back_label = Label(self.font, 24, "BACK", "darkgreen", {"center": (0, 0)}, "white")
        b_width = 140
        b_height = 60
        self.back_button = Button(menu.centerx - b_width/2,
                                                menu.bottom - (20 + b_height),
                                                b_width, b_height, back_label)
        
        types = ["Rest", "Merrymaking", "Feasting", "Resource", "Production",
                      "Utility", "Decorations"]
        self.buttons = []
        b_width = 120
        b_height = 40
        space = 10
        top = self.title_label.rect.bottom + 10
        left = menu.centerx - b_width/2
        for t in types:
            t_label = Label(self.font, 16, t, "gray1", {"center": (0, 0)}, "white")
            self.buttons.append(PayloadButton(left, top, b_width, b_height,
                                          t_label, t))
            top += b_height + space                                    
            
    def startup(self, persistent):
        self.persist = persistent
        if self.persist["helping"]:
            self.cursor = prepare.GFX["questionmark"]
        else:
            self.cursor = prepare.GFX["hammercursor"]
       
        
    def draw(self, surface):
        self.persist["world"].draw(surface)
        self.menu.draw(surface)
        self.title_label.draw(surface)
        self.back_button.draw(surface)
        for button in self.buttons:
            button.draw(surface)
        surface.blit(self.cursor, pg.mouse.get_pos())
        
    def update(self, surface, keys, dt):
        self.draw(surface) 
    
    def get_event(self, event):
        if event.type == pg.QUIT:
            self.next = "MANAGING"
            self.done = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.back_button.rect.collidepoint(event.pos):
                    if self.persist["helping"]:
                        self.next  = "HELPMENU"
                    else:
                        self.next = "MANAGING"
                    self.done = True
                else:
                    for button in self.buttons:
                        if button.rect.collidepoint(event.pos):
                            self.persist["building type"] = button.payload
                            self.next = "BUILDINGSELECTION"
                            self.done = True 
                            break                        
            elif event.button == 3:
                if self.persist["helping"]:
                    self.next = "HELPMENU"
                else:
                    self.next = "MANAGING"
                self.done = True                
                    