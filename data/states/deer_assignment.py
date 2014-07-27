from itertools import cycle
import pygame as pg
from .. import tools, prepare
from ..components.labels import Label

class DeerAssignment(tools._State):
    def __init__(self):
        super(DeerAssignment, self).__init__()
        self.next = "MANAGING"
        
    def startup(self, persistent):
        self.next = "MANAGING"
        self.persist = persistent
        self.deer = self.persist["deer"]
        self.world = self.persist["world"]
        pg.mouse.set_visible(False)
        screen = pg.display.get_surface().get_rect()
        self.cursors = cycle([prepare.GFX["leftreindeer1"], prepare.GFX["leftreindeer2"]])
        self.cursor = next(self.cursors)
        font = prepare.FONTS["weblysleekuili"]
        self.instruct_label = Label(font, 14, "Left-click a barn to assign reindeer", "gray1",
                                               {"midtop": (screen.centerx, screen.top + 5)})
        self.instruct_label2 = Label(font, 14, "Right-click to cancel", "gray1",
                                                {"midtop": (screen.centerx,
                                                                  self.instruct_label.rect.bottom + 5)})
        self.ticks = 0
        
    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                for b in [x for x in self.world.buildings if x.name == "Barn"]:
                    if b.rect.collidepoint(event.pos):
                        if len(b.reindeers) < 10:
                            self.deer.barn.reindeers.remove(self.deer)
                            self.deer.rect.center = b.rect.center
                            self.deer.barn = b
                            b.reindeers.append(self.deer)
                            self.done = True
                            break
            elif event.button == 3:
                self.done = True
                
    def update(self, surface, keys):
        self.ticks += 1
        if not self.ticks % 8:
            self.cursor = next(self.cursors)
        self.draw(surface)
        
    def draw(self, surface):
        self.world.draw(surface)
        self.instruct_label.draw(surface)
        surface.blit(self.cursor, pg.mouse.get_pos())
        