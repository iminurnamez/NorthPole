import itertools as it
import pygame as pg
from .. import tools, prepare
from ..components.labels import GroupLabel as GLabel
from ..components.labels import Label, Meter, Button

class ElfPopup(tools._State):
    def __init__(self):
        
        super(ElfPopup, self).__init__()
        self.font = prepare.FONTS["weblysleekuil"]
        self.cursor = prepare.GFX["canecursor"]
        center = pg.display.get_surface().get_rect().center
        self.popup = pg.Rect(0, 0, 400, 500)
        self.popup.center = center
        a_label = Label(self.font, 16, "Assign", "gray1",
                               {"center": (0, 0)}, "white")
        self.assign_button = Button(self.popup.left + 50,
                                                  self.popup.top + 400,
                                                  80, 30, a_label)
        done_label = Label(self.font, 18, "DONE", "gray1", 
                                     {"topleft": (0, 0)}, "white")
        self.done_button = Button(self.popup.centerx - 40,
                                                self.popup.bottom - 60, 80, 40,
                                                done_label)
    
    def draw(self, surface):
        self.world.draw(surface)
        pg.draw.rect(surface, pg.Color("white"), self.popup)
        pg.draw.rect(surface, pg.Color("darkred"), self.popup, 3)
        for thing in it.chain(self.meters, self.labels):
            thing.draw(surface)
        self.assign_button.draw(surface)
        self.done_button.draw(surface)
        surface.blit(self.cursor, pg.mouse.get_pos())
        
    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.done_button.rect.collidepoint(event.pos):
                    self.next = self.persist["previous"]
                    self.done = True            
                elif self.assign_button.rect.collidepoint(event.pos):
                    self.next = "ELFASSIGNMENT"
                    self.done = True
            elif event.button == 3:
                self.next = self.persist["previous"]
                self.done = True
                
    def update(self, surface, keys):
        self.draw(surface)    
        
    def startup(self, persistent):
        pg.mouse.set_visible(False)
        job_map = {"Warehouse": "Hauler",
                           "Moss Farm": "Moss Farmer",
                           "Carrot Farm": "Carrot Farmer",
                           "Beet Farm": "Beet Farmer",
                           "Barn": "Reindeer Wrangler",
                           "Wood Shed": "Lumberjack",
                           "Bakery": "Baker",
                           "Mine": "Miner",
                           "Sawmill": "Miller",
                           "Nursery": "Arborist",
                           "Dentist's Office": "Dentist",
                           "Schoolhouse": "Student"}
        
        self.persist = persistent
        self.world = self.persist["world"]
        self.elf = self.persist["elf"]
        self.next = self.persist["previous"]
        
        
        
        elf = self.elf
        self.labels = []
        name_label = GLabel(self.labels, self.font, 20, elf.name, "gray1", 
                                        {"midtop": (self.popup.centerx, self.popup.top + 5)},
                                        "white")
        
        if elf.job is None:
            job_name = "Unemployed"
        else:
            job_name = job_map[elf.job.name]
        career_label = GLabel(self.labels, self.font, 16, job_name,
                                         "gray1", {"midtop": (self.popup.centerx,
                                         name_label.rect.bottom + 2)}, "white")
        if elf.state in {"Travelling", "Hauling"}:
            activity = "{} to {}".format(elf.state, elf.venue.name)
        else:
            activity = "{}".format(elf.state)        
        activity_label = GLabel(self.labels, self.font, 14, activity, "gray1", {"midtop": 
                                          (self.popup.centerx, career_label.rect.bottom + 3)},
                                          "white")
        elf_stats = [("Energy", elf.energy/float(elf.max_energy)),
                          ("Food", elf.food/float(elf.max_food)),
                          ("Cheer", elf.cheer/float(elf.max_cheer)),
                          ("Cavities", elf.cavities/float(elf.max_cavities))]   
        meter_left = self.popup.left + 100
        meter_middle = activity_label.rect.bottom + 10
        label_left = self.popup.left + 10
        self.meters = []
        for stat in elf_stats:
            meter = Meter((meter_left, meter_middle), 150, 10, stat[1])
            self.meters.append(meter)
            stat_label = GLabel(self.labels, self.font, 14, stat[0], "gray1", 
                                         {"midleft": (label_left, meter_middle)}, "white")
            meter_middle += 20
        skill_title = GLabel(self.labels, self.font, 20, "Skills", "gray1", {"midtop":
                                      (self.popup.centerx, stat_label.rect.bottom + 10)},
                                      "white")
        meter_middle = skill_title.rect.bottom + 10
        for skill in elf.skills:
            meter = Meter((meter_left, meter_middle), 150, 10, elf.skills[skill])
            self.meters.append(meter)
            skill_label = GLabel(self.labels, self.font, 14, skill, "gray1",
                                         {"midleft": (label_left, meter_middle)}, "white")
            meter_middle += 20