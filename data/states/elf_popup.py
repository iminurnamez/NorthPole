import itertools as it
import pygame as pg
from .. import tools, prepare
from ..components.labels import GroupLabel as GLabel
from ..components.labels import Label, Meter, Button

class ElfPopup(tools._State):
    def __init__(self):
        super(ElfPopup, self).__init__()
        center = pg.display.get_surface().get_rect().center
        self.popup = pg.Rect(0, 0, 400, 500)
        self.popup.center = center
        done_label = Label(18, "DONE", "gray1", "topleft", 
                                     0, 0, "lightgray")
        self.done_button = Button(self.popup.centerx - 40,
                                                self.popup.bottom - 60, 80, 50,
                                                done_label)
    
    def display(self, surface):
        pg.draw.rect(surface, pg.Color("white"), self.popup)
        pg.draw.rect(surface, pg.Color("darkred"), self.popup, 3)
        for thing in it.chain(self.meters, self.labels):
            thing.display(surface)
        self.done_button.display(surface)
        
    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.done_button.rect.collidepoint(event.pos):
                self.done = True            
    
    def update(self, surface, keys):
        self.display(surface)    
        
    def startup(self, persistant):
        job_map = {"Warehouse": "Hauler",
                           "Moss Farm": "Moss Farmer",
                           "Carrot Farm": "Carrot Farmer",
                           "Barn": "Reindeer Wrangler",
                           "Wood Shed": "Lumberjack"}
        self.player = persistant["player"]
        elf = persistant["elf"]
        self.next = persistant["previous"]
        self.labels = []
        name_label = GLabel(self.labels, 24, elf.name, "gray1", "midtop",
                                        self.popup.centerx, self.popup.top + 10,
                                        "white")
        
        career_label = GLabel(self.labels, 18, job_map[elf.job.name],
                                         "gray1", "midtop", self.popup.centerx,
                                         name_label.rect.bottom + 5, "white")
        if elf.state in {"Travelling", "Hauling"}:
            activity = "{} to {}".format(elf.state, elf.venue.name)
        else:
            activity = "{}".format(elf.state)        
        activity_label = GLabel(self.labels, 14, activity, "gray1", "midtop", 
                                           self.popup.centerx,
                                           career_label.rect.bottom + 5, "white")
        elf_stats = [("Energy", elf.energy/elf.max_energy),
                          ("Food", elf.food/elf.max_food),
                          ("Cheer", elf.cheer/elf.max_cheer)]   
        meter_left = self.popup.left + 100
        meter_middle = activity_label.rect.bottom + 20
        label_left = self.popup.left + 10
        self.meters = []
        for stat in elf_stats:
            meter = Meter((meter_left, meter_middle), 150, 10, stat[1])
            self.meters.append(meter)
            stat_label = GLabel(self.labels, 14, stat[0], "gray1", "midleft",
                                          label_left, meter_middle, "white")
            meter_middle += 30
        
        return tools._State.startup(self, persistant)    
    
    def cleanup(self):
        self.persist["player"] = self.player
        self.done = False
        return self.persist
       
