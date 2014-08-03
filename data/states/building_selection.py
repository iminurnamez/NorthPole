import pygame as pg
from .. import tools, prepare
from ..components import buildings, decorations, landing_strip, sawmill, nursery, dentist, school
from ..components.labels import Label, GroupLabel, Button, PayloadButton


class BuildingSelection(tools._State):
    def __init__(self):
        super(BuildingSelection, self).__init__()
        self.cursor = prepare.GFX["hammercursor"]
        self.next = "BUILDINGPLACEMENT"
        self.font = prepare.FONTS["weblysleekuil"]
        screen_rect = pg.display.get_surface().get_rect()
        self.window = pg.Rect(0, 0, 400, 500)
        self.window.center = screen_rect.center
        self.title = Label(self.font, 24, "Select a building to construct", "darkgreen",
                                 {"midtop": (self.window.centerx, self.window.top + 10)},
                                 "white")
        b_label = Label(self.font, 24, "BACK", "gray1", {"center": (0, 0)}, "white")
        self.back = Button(self.window.centerx - 50, self.window.bottom - 90, 120, 70, b_label)
    
    def startup(self, persistent):
        build_map = {"Rest": [buildings.Igloo, buildings.House, buildings.GingerbreadHouse],
                             "Merrymaking": [buildings.Theater, buildings.SnowForts,
                                                      buildings.SkatingRink],
                             "Feasting": [buildings.SnackBar, buildings.CarrotStand,
                                               buildings.CottonCandyCart],
                             "Resource": [buildings.MossFarm, buildings.CarrotFarm,
                                                buildings.BeetFarm, buildings.WoodShed, nursery.Nursery],
                             "Production": [buildings.Barn, buildings.Bakery, sawmill.Sawmill],
                             "Utility": [buildings.Warehouse, landing_strip.LandingStrip, dentist.DentistOffice, school.School],
                             "Decorations": [decorations.Snowman, decorations.XmasTree,
                                                    decorations.WavySanta, decorations.PyroBox]}
        self.persist = persistent
        self.build_type = persistent["building type"]
        self.world = self.persist["world"]
        if self.persist["helping"]:
            self.cursor = prepare.GFX["questionmark"]
        else:
            self.cursor = prepare.GFX["hammercursor"]
        self.buttons = []
        top = self.title.rect.bottom + 30
        for build in build_map[self.build_type]:
            label = Label(self.font, 16, build.name, "gray1", {"center": (0, 0)}, "white")
            button = PayloadButton(self.window.centerx - 70, top, 140, 50, label, build)
            
            top += button.rect.height + 20
            self.buttons.append(button)
    
    
    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.back.rect.collidepoint:
                    self.next = "BUILDINGTYPESELECTION"
                    self.done = True
                for button in self.buttons:
                    if button.rect.collidepoint(event.pos):
                        self.persist["building type"] = button.payload
                        if self.persist["helping"]:
                            self.next = "BUILDINGHELP"
                        else:
                            self.next = "BUILDINGPLACEMENT"
                        self.done = True
                        break
            elif event.button == 3:
                self.next = "BUILDINGTYPESELECTION"
                self.done = True
                
    def update(self, surface, keys, dt):
        self.draw(surface)
        
    def draw(self, surface):
        self.world.draw(surface)
        pg.draw.rect(surface, pg.Color("white"), self.window)
        pg.draw.rect(surface, pg.Color("maroon"), self.window, 3)
        self.title.draw(surface)
        self.back.draw(surface)
        for button in self.buttons:
            button.draw(surface)
        surface.blit(self.cursor, pg.mouse.get_pos())