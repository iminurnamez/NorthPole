import pygame as pg
from .. import tools, prepare
from ..components.labels import Label, GroupLabel as GLabel, Meter, Button


class DeerPopup(tools._State):
    def __init__(self):
        super(DeerPopup, self).__init__()
        self.next = "MANAGING"
        self.window = pg.Rect(0, 0, 400, 400)
        self.window.center = pg.display.get_surface().get_rect().center
        self.font = prepare.FONTS["weblysleekuil"]
        done_label = Label(self.font, 18, "DONE", "gray1", {"topleft": (0, 0)},
                                     "white")
        self.done_button = Button(self.window.centerx - 40,
                                                self.window.bottom - 60, 80, 50,
                                                done_label)
        
    def startup(self, persistent):
        self.persist = persistent
        self.deer = self.persist["deer"]
        deer = self.deer
        self.labels = []
        name_label = GLabel(self.labels, self.font, 20, self.deer.name, "gray1", 
                                        {"midtop": (self.window.centerx, self.window.top + 5)},
                                        "white")
        deer_stats = [("Speed", deer.speed/100.0),
                             ("Stamina", deer.stamina/100.0)]   
        meter_left = self.window.left + 100
        meter_middle = name_label.rect.bottom + 10
        label_left = self.window.left + 10
        self.meters = []
        for stat in deer_stats:
            meter = Meter((meter_left, meter_middle), 150, 10, stat[1])
            self.meters.append(meter)
            stat_label = GLabel(self.labels, self.font, 14, stat[0], "gray1", 
                                         {"midleft": (label_left, meter_middle)}, "white")
            meter_middle += 20
        self.price = int(((deer.speed**2) / 8.0) + ((deer.stamina**2) / 12.0))  
        sell = Label(self.font, 16, "Sell for ${}".format(self.price), "gray1", {"topleft": (0, 0)})
        self.sell_button = Button(self.window.centerx + 20,
                                              self.window.bottom - 100,
                                              sell.rect.width + 10,
                                              sell.rect.height + 6, sell)
        assign = Label(self.font, 16, "Assign", "gray1", {"topleft": (0, 0)})
        self.assign_button = Button(self.window.centerx - (assign.rect.width + 20),
                                                  self.window.bottom - 100,
                                                  assign.rect.width + 10,
                                                  assign.rect.height + 6, assign)

    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.done_button.rect.collidepoint(event.pos):
                    self.next = "MANAGING"
                    self.done = True
                elif self.sell_button.rect.collidepoint(event.pos):
                    self.deer.barn.reindeers.remove(self.deer)
                    self.persist["player"].cash += self.price
                    self.done = True
                elif self.assign_button.rect.collidepoint(event.pos):
                    self.next = "DEERASSIGNMENT"
                    self.done = True
            elif event.button == 3:
                self.next = "MANAGING"
                self.done = True
                
    def update(self, surface, keys, dt):
        self.draw(surface)
    
    def draw(self, surface):
        pg.draw.rect(surface, pg.Color("white"), self.window)
        pg.draw.rect(surface, pg.Color("maroon"), self.window, 3)
        for label in self.labels:
            label.draw(surface)
        for meter in self.meters:
            meter.draw(surface)
        self.sell_button.draw(surface)
        self.assign_button.draw(surface)
        self.done_button.draw(surface)
        