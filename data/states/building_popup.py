import pygame as pg
from .. import tools, prepare
from ..components.labels import GroupLabel as GLabel, Label
from ..components.labels import Label, Meter, Button

class BuildingPopup(tools._State):
    
    def __init__(self):
        super(BuildingPopup, self).__init__()
        self.cursor = prepare.GFX["canecursor"]
        center = pg.display.get_surface().get_rect().center
        self.popup = pg.Rect(0, 0, 400, 500)
        self.popup.center = center
        self.font = prepare.FONTS["weblysleekuil"]
        done_label = Label(self.font, 18, "DONE", "gray1", {"topleft": (0, 0)},
                                     "white")
        self.done_button = Button(self.popup.centerx - 40,
                                                self.popup.bottom - 60, 80, 50,
                                                done_label)
    
    def draw(self, surface):
        self.world.draw(surface)
        pg.draw.rect(surface, pg.Color("white"), self.popup)
        pg.draw.rect(surface, pg.Color("darkred"), self.popup, 3)
        for label in self.labels:
            label.draw(surface)
        if self.persist["building"].modes:
            self.mode_label.draw(surface)
            surface.blit(self.left_arrow, self.left_arrow_rect)
            surface.blit(self.right_arrow, self.right_arrow_rect)
        for blitter in self.blitters:
            surface.blit(blitter[0], blitter[1])
        self.done_button.draw(surface)
        surface.blit(self.cursor, pg.mouse.get_pos())
        
    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                building = self.persist["building"]
                if building.modes:
                    if self.left_arrow_rect.collidepoint(event.pos):
                        for _ in range(len(building.modes) - 1):
                            building.mode = next(building.mode_cycle)
                    elif self.right_arrow_rect.collidepoint(event.pos):
                        building.mode = next(building.mode_cycle)
                if self.done_button.rect.collidepoint(event.pos):
                    if self.persist["previous"] == "BUILDINGPOPUP":
                        self.next = "MANAGING"
                    self.done = True
                for spot in self.worker_spots:
                    if spot[1].collidepoint(event.pos):
                        self.persist["elf"] = spot[0]
                        self.persist["previous"] = "BUILDINGPOPUP"
                        self.next = "ELFPOPUP"
                        self.done = True                        
            elif event.button == 3:
                if self.persist["previous"] == "BUILDINGPOPUP":
                    self.next = "MANAGING"
                self.done = True
                
    def update(self, surface, keys):
        if self.persist["building"].modes:
            self.mode_label = Label(self.font, 18, self.persist["building"].mode, "gray1",
                                                {"midtop": (self.popup.centerx,
                                                                  self.name_label.rect.bottom + 3)})
            self.left_arrow_rect = self.left_arrow.get_rect(midright=(self.mode_label.rect.left - 10,
                                                                                               self.mode_label.rect.centery))
            self.right_arrow_rect = self.right_arrow.get_rect(midleft=(self.mode_label.rect.right + 10,
                                                                                                 self.mode_label.rect.centery))
        self.draw(surface)    
        
    def startup(self, persistent):
        pg.mouse.set_visible(False)
        self.persist = persistent
        self.player = persistent["player"]
        self.world = persistent["world"]
        building = persistent["building"]
        self.building = building
        self.next = persistent["previous"]
        self.labels = []
        self.blitters = []
        self.name_label = GLabel(self.labels, self.font, 24, building.name, "gray1",
                                              {"midtop": (self.popup.centerx, self.popup.top + 10)},
                                              "white")
        current_bottom = self.name_label.rect.bottom
        if building.modes:
            self.mode_label = Label(self.font, 18, self.persist["building"].mode, "gray1",
                                                {"midtop": (self.popup.centerx, current_bottom + 3)})
            current_bottom =  self.mode_label.rect.bottom
            self.left_arrow = prepare.GFX["leftarrow"]
            self.left_arrow_rect = self.left_arrow.get_rect(midright=(self.mode_label.rect.left - 10,
                                                                                               self.mode_label.rect.centery))
            self.right_arrow = pg.transform.flip(self.left_arrow, True, False)
            self.right_arrow_rect = self.right_arrow.get_rect(midleft=(self.mode_label.rect.right + 10,
                                                                                                 self.mode_label.rect.centery))
                       
        empty_cameo = prepare.GFX["blankcameo"]
        elf_cameo = prepare.GFX["elfcameo"]
        cameo_rect = empty_cameo.get_rect()
        
        w = cameo_rect.width
        bmw = building.max_workers
        bmp = building.max_patrons
        self.worker_spots = []
        if bmw:
            word = "Students" if building.name == "Schoolhouse" else "Workers"
            worker_title = GLabel(self.labels, self.font, 16, word, "gray1",
                                             {"midtop": (self.popup.centerx,
                                               current_bottom + 10)}, "white")
            
            if bmw <= 8:
                worker_surf = pg.Surface((w * bmw,
                                                  cameo_rect.height)).convert()
                for i in range(bmw):
                    worker_surf.blit(empty_cameo, (w * i, 0))
                for j, elf in enumerate(building.workers):
                    worker_surf.blit(elf_cameo, (w * j, 0))
                    self.worker_spots.append((elf, elf_cameo.get_rect(
                                                            topleft=(self.popup.centerx - (worker_surf.get_width()/2) + (w*j),
                                                            worker_title.rect.bottom + 5))))
                    
            else:
                top_num = (bmw / 2) + bmw % 2
                bottom_num = bmw / 2
                worker_surf = pg.Surface((w * top_num,
                                                  cameo_rect.height * 2)).convert()
                if len(building.workers) <= top_num:
                    top_worker_num = len(building.workers)
                    bottom_worker_num = 0
                else:
                    top_worker_num = top_num
                    bottom_worker_num = len(building.workers) - top_num
                
                for num in range(top_num):
                    worker_surf.blit(empty_cameo, (w * num, 0))
                for tw_num in range(top_worker_num):
                    worker_surf.blit(elf_cameo, (w * tw_num, 0))
                    self.worker_spots.append((building.workers[tw_num],
                                                            elf_cameo.get_rect(
                                                            topleft=(self.popup.centerx  - (worker_surf.get_width()/2) + (w*tw_num),
                                                                         worker_title.rect.bottom + 5))))                  
                
                offset = int((top_num - bottom_num) * (w / 2))
                for b_num in range(bottom_num):
                    worker_surf.blit(empty_cameo, (offset + (w * b_num),
                                                              cameo_rect.height))  
                for bw_num in range(bottom_worker_num):
                    worker_surf.blit(elf_cameo, (offset + (w * bw_num),
                                                         cameo_rect.height))
                    self.worker_spots.append((building.workers[top_worker_num + bw_num], 
                                                           elf_cameo.get_rect(
                                                           topleft=(self.popup.centerx + offset - (worker_surf.get_width()/2) + (w*bw_num),
                                                                        cameo_rect.height + worker_title.rect.bottom + 5))))                  
            workers_rect = worker_surf.get_rect(midtop=(self.popup.centerx,
                                                             worker_title.rect.bottom + 5))
            worker_surf.set_colorkey(pg.Color("black"))
            self.blitters.append((worker_surf, workers_rect))
            current_bottom = workers_rect.bottom
        if bmp:
            
            top = current_bottom + 10
            patron_title = GLabel(self.labels, self.font, 16, "Patrons", "gray1",
                                            {"midtop": (self.popup.centerx, top)},
                                            "white")
            if bmp <= 8:
                patrons = pg.Surface((w * bmp,
                                           cameo_rect.height)).convert()
                
                for i in range(bmp):
                    patrons.blit(empty_cameo, (w * i, 0))
                for j, elf in enumerate(building.patrons):
                    patrons.blit(elf_cameo, (w * j, 0))
                    self.worker_spots.append((elf,
                            elf_cameo.get_rect(topleft=(self.popup.centerx - (patrons.get_width()/2) + (w*j),
                                                                      patron_title.rect.bottom + 10))))
                
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
                    self.worker_spots.append((building.patrons[tw_num],
                                                            elf_cameo.get_rect(
                                                            topleft=(self.popup.centerx - (patrons.get_width()/2) + (w*tw_num),
                                                                         patron_title.rect.bottom + 10))))                    
                offset = int((top_num - bottom_num) * (w / 2))
                for b_num in range(bottom_num):
                    patrons.blit(empty_cameo, (offset + (w * b_num),
                                                              cameo_rect.height))  
                for bw_num in range(bottom_worker_num):
                    patrons.blit(elf_cameo, (offset + (w * bw_num),
                                                        cameo_rect.height))
                    self.worker_spots.append((building.patrons[top_worker_num + bw_num],
                                                          elf_cameo.get_rect(
                                                          topleft=(self.popup.centerx - (patrons.get_width()/2) + (w*bw_num),
                                                                       patron_title.rect.bottom + 10) + cameo_rect.height)))
            patrons_rect = patrons.get_rect(midtop=(self.popup.centerx,
                                                            patron_title.rect.bottom + 10))
            patrons.set_colorkey(pg.Color("black"))
            self.blitters.append((patrons, patrons_rect))           
            current_bottom = patrons_rect.bottom
        top = current_bottom + 20
        left = self.popup.left + 50
        spacer = 200
        if building.inputs:
            input_title = GLabel(self.labels, self.font, 16, "Inputs", "gray1", {"midtop":
                                          (self.popup.centerx, top)}, "white")                               
            top += input_title.rect.height + 10
            i = 0
            for thing in building.inputs:
                thing_label = GLabel(self.labels, self.font, 12, "{:20}{:.2f}".format(
                                                thing, building.inputs[thing]), "gray1",
                                                {"topleft": (left + ((i % 2) * spacer), top)},
                                                "white")
                if i % 2:
                    top += thing_label.rect.height + 5                
                i += 1
                
            if i % 2:
                top += thing_label.rect.height + 10
            else:
                top += 10            
        
        if building.outputs:
            output_title = GLabel(self.labels, self.font, 16, "Outputs", "gray1", 
                                            {"midtop": (self.popup.centerx, top)}, "white")
            top += output_title.rect.height + 10
            i = 0
            for item in building.outputs:
                item_label = GLabel(self.labels, self.font, 12, "{:20}{:.2f}".format(
                                                item, building.outputs[item]), "gray1",
                                                {"topleft": (left + ((i % 2) * spacer), top)},
                                                "white")
                if i % 2:
                    top += item_label.rect.height + 5                
                i += 1
    
 
