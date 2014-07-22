import pygame as pg
from .. import prepare, tools
from ..components.labels import Label, GroupLabel as GLabel, Button


class ElfSelector(tools._State):
    def __init__(self):
        super(ElfSelector, self).__init__()
        self.font = prepare.FONTS["weblysleekuil"]
        screen = pg.display.get_surface().get_rect()
        self.window = pg.Rect(0, 0, 400, 500)
        self.window.center = screen.center
        self.title = Label(self.font, 24, "Click on an elf's name to select",
                                 "darkgreen", {"midtop": (self.window.centerx, self.window.top + 10)},
                                 "white")
        back_label = Label(self.font, 24, "BACK", "darkgreen", {"center": (0, 0)}, "white")
        b_width = 140
        b_height = 60
        self.back_button = Button(self.window.centerx - b_width/2,
                                               self.window.bottom - (20 + b_height),
                                               b_width, b_height, back_label)
        self.cursor = prepare.GFX["canecursor"]
                                                
    def startup(self, persistent):
        pg.mouse.set_visible(False)
        self.persist = persistent
        self.world = self.persist["world"]
        # only first ten elves
        self.elves = self.persist["elves"]
        if len(self.elves) > 10:
            self.elves = self.elves[:10]
        top = self.title.rect.bottom + 20
        self.labels = []
        for elf in self.elves:
            elf.name_label = GLabel(self.labels, self.font, 16, elf.name, "gray1",
                                                 {"midtop": (self.window.centerx, top)},
                                                 "white")                                                 
            top += elf.name_label.rect.height + 10
        
    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.back_button.rect.collidepoint(event.pos):
                    self.done = True
                    self.next = "MANAGING"
                else:
                    for elf in self.elves:
                        if elf.name_label.rect.collidepoint(event.pos):
                            self.next = "ELFPOPUP"
                            self.persist["elf"] = elf
                            self.done = True
                            break
            elif event.button == 3:
                self.done = True
                self.next = "MANAGING"
                
    def update(self, surface, keys):
        self.draw(surface)
        
    def draw(self, surface):
        self.world.draw(surface)
        pg.draw.rect(surface, pg.Color("white"), self.window)
        pg.draw.rect(surface, pg.Color("maroon"), self.window, 3)
        self.title.draw(surface)
        for label in self.labels:
            label.draw(surface)
        self.back_button.draw(surface)
        surface.blit(self.cursor, pg.mouse.get_pos())