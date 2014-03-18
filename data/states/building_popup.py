import pygame as pg
from .. import tools, prepare
from ..components.labels import GroupLabel as GLabel
from ..components.labels import Label, Meter, Button

class BuildingPopup(tools._State):
    def __init__(self):
        super(BuildingPopup, self).__init__()
        center = pg.display.get_surface().get_rect().center
        self.popup = pg.Rect(0, 0, 400, 500)
        self.popup.center = center
        done_label = Label(18, "DONE", "gray1", "topleft", 0, 0,
                                     "lightgray")
        self.done_button = Button(self.popup.centerx - 40,
                                                self.popup.bottom - 60, 80, 50,
                                                done_label)
    
    def display(self, surface):
        pg.draw.rect(surface, pg.Color("white"), self.popup)
        pg.draw.rect(surface, pg.Color("darkred"), self.popup, 3)
        for label in self.labels:
            label.display(surface)
        for blitter in self.blitters:
            surface.blit(blitter[0], blitter[1])
        self.done_button.display(surface)
        
    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.done_button.rect.collidepoint(event.pos):
                self.done = True            
    
    def update(self, surface, keys):
        self.display(surface)    
        
    def startup(self, persistant):
        self.player = persistant["player"]
        building = persistant["building"]
        self.next = persistant["previous"]
        self.labels = []
        self.blitters = []
        name_label = GLabel(self.labels, 24, building.name, "gray1",
                                        "midtop", self.popup.centerx,
                                        self.popup.top + 10, "white")
        empty_cameo = prepare.GFX["blankcameo"]
        elf_cameo = prepare.GFX["elfcameo"]
        cameo_rect = empty_cameo.get_rect()
        
        w = cameo_rect.width
        bmw = building.max_workers
        bmp = building.max_patrons
        
        if bmw:
            worker_title = GLabel(self.labels, 16, "Workers", "gray1",
                                             "midtop", self.popup.centerx,
                                             name_label.rect.bottom + 10, "white")
            if bmw <= 8:
                workers = pg.Surface((w * bmw,
                                                  cameo_rect.height)).convert()
                for i in range(bmw):
                    workers.blit(empty_cameo, (w * i, 0))
                for j in range(len(building.workers)):
                    workers.blit(elf_cameo, (w * j, 0))
            else:
                top_num = (bmw / 2) + bmw % 2
                bottom_num = bmw / 2
                workers = pg.Surface((w * top_num,
                                                  cameo_rect.height * 2)).convert()
                if len(building.workers) <= top_num:
                    top_worker_num = len(building.workers)
                    bottom_worker_num = 0
                else:
                    top_worker_num = top_num
                    bottom_worker_num = len(building.workers) - top_num
                
                for num in range(top_num):
                    workers.blit(empty_cameo, (w * num, 0))
                for tw_num in range(top_worker_num):
                    workers.blit(elf_cameo, (w * tw_num, 0))        
                
                offset = int((top_num - bottom_num) * (w / 2))
                for b_num in range(bottom_num):
                    workers.blit(empty_cameo, (offset + (w * b_num),
                                                              cameo_rect.height))  
                for bw_num in range(bottom_worker_num):
                    workers.blit(elf_cameo, (offset + (w * bw_num),
                                                         cameo_rect.height))
            workers_rect = workers.get_rect(midtop=(self.popup.centerx,
                                                             worker_title.rect.bottom + 5))
            workers.set_colorkey(pg.Color("black"))
            self.blitters.append((workers, workers_rect))

        if bmp:
            if bmw:
                top = workers_rect.bottom + 10
            else:
                top = name_label.rect.bottom + 10
            patron_title = GLabel(self.labels, 16, "Patrons", "gray1",
                                            "midtop", self.popup.centerx, top,
                                        "white")
            if bmp <= 8:
                patrons = pg.Surface((w * bmp,
                                           cameo_rect.height)).convert()
                
                for i in range(bmp):
                    patrons.blit(empty_cameo, (w * i, 0))
                for j in range(len(building.patrons)):
                    patrons.blit(elf_cameo, (w * j, 0))
                
            else:
                top_num = (bmp / 2) + bmp % 2
                bottom_num = bmp / 2
                patrons = pg.Surface((w * top_num,
                                                  cameo_rect.height * 2)).convert()
                
                if len(building.patrons) <= top_num:
                    top_worker_num = len(building.patrons)
                    bottom_worker_num = 0
                else:
                    top_worker_num = top_num
                    bottom_worker_num = len(building.patrons) - top_num
                for num in range(top_num):
                    patrons.blit(empty_cameo, (w * num, 0))
                for tw_num in range(top_worker_num):
                    patrons.blit(elf_cameo, (w * tw_num, 0))        
                offset = int((top_num - bottom_num) * (w / 2))
                for b_num in range(bottom_num):
                    patrons.blit(empty_cameo, (offset + (w * b_num),
                                                              cameo_rect.height))  
                for bw_num in range(bottom_worker_num):
                    patrons.blit(elf_cameo, (offset + (w * bw_num),
                                                        cameo_rect.height))
            patrons_rect = patrons.get_rect(midtop=(self.popup.centerx,
                                                            patron_title.rect.bottom + 10))
            patrons.set_colorkey(pg.Color("black"))
            self.blitters.append((patrons, patrons_rect))           
            
        top = self.popup.top + 150
        left = self.popup.left + 50
        spacer = 200
        if building.inputs:
            input_title = GLabel(self.labels, 16, "Inputs", "gray1", "midtop",
                                          self.popup.centerx, top, "white")                               
            top += input_title.rect.height + 10
            i = 0
            for thing in building.inputs:
                thing_label = GLabel(self.labels, 12, "{:20}{:.2f}".format(
                                                thing, building.inputs[thing]), "gray1",
                                                "topleft", left + ((i % 2) * spacer), top,
                                                "white")
                if i % 2:
                    top += thing_label.rect.height + 5                
                i += 1
                
            if i % 2:
                top += thing_label.rect.height + 10
            else:
                top += 10            
        
        if building.outputs:
            output_title = GLabel(self.labels, 16, "Outputs", "gray1", "midtop",
                                             self.popup.centerx, top, "white")
            top += output_title.rect.height + 10
            i = 0
            for item in building.outputs:
                item_label = GLabel(self.labels, 12, "{:20}{:.2f}".format(
                                                item, building.outputs[item]), "gray1",
                                                "topleft", left + ((i % 2) * spacer), top,
                                                "white")
                if i % 2:
                    top += item_label.rect.height + 5                
                i += 1

        return tools._State.startup(self, persistant)    
    
    def cleanup(self):
        self.persist["player"] = self.player
        self.done = False
        return self.persist
       
