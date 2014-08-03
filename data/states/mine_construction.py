import pygame as pg
from .. import tools, prepare
from ..components.labels import Label, Button
from ..components.buildings import Mine


class MineConstruction(tools._State):
    def __init__(self):
        super(MineConstruction, self).__init__()
        self.next = "MANAGING"
        self.cursor = prepare.GFX["canecursor"]
        center = pg.display.get_surface().get_rect().center
        self.window = pg.Rect(0, 0, 400, 500)
        self.window.center = center
        font = prepare.FONTS["weblysleekuil"]
        self.title = Label(font, 16, "Ore Deposit", "darkgreen",
                                 {"midtop": (self.window.centerx, self.window.top + 10)},
                                 "white")
        build = Label(font, 16, "Build Mine", "darkgreen", {"topleft": (0, 0)},
                                     "white")
        self.build_button = Button(self.window.centerx - 60,
                                                self.title.rect.bottom + 20, 120, 50,
                                                build)                             
        done_label = Label(font, 18, "DONE", "darkgreen", {"topleft": (0, 0)},
                                     "white")
        self.done_button = Button(self.window.centerx - 40,
                                                self.window.bottom - 60, 80, 50,
                                                done_label) 
        
    def startup(self, persistent):
        self.next = "MANAGING"
        self.persist = persistent
        self.world = self.persist["world"]
        self.player = self.persist["player"]
        self.ore = self.persist["ore"]
        
    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.done_button.rect.collidepoint(event.pos):
                    self.done = True
                elif self.build_button.rect.collidepoint(event.pos):
                    new_mine = Mine(self.ore.index, self.world)
                    self.world.ores.remove(self.ore)
                    self.done = True
            elif event.button == 3:
                self.done = True

    def update(self, surface, keys, dt):
        self.draw(surface)
    
    def draw(self, surface):
        self.world.draw(surface)
        pg.draw.rect(surface, pg.Color("white"), self.window)
        pg.draw.rect(surface, pg.Color("maroon"), self.window, 3)
        self.title.draw(surface)
        self.build_button.draw(surface)
        self.done_button.draw(surface)
        surface.blit(self.cursor, pg.mouse.get_pos())