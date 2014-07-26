import pygame as pg
from .. import tools, prepare
from ..components.labels import Label

class ElfAssignment(tools._State):
    def __init__(self):
        super(ElfAssignment, self).__init__()
        self.cursor = prepare.GFX["canecursor"]
        self.next = "MANAGING"
        screen = pg.display.get_surface().get_rect()
        font = prepare.FONTS["weblysleekuili"]
        self.instruct_label = Label(font, 14, "Left-click a building to assign elf",
                                              "gray1", {"midtop": (screen.centerx, screen.top + 5)})
        self.instruct_label2 = Label(font, 14, "Right-click to cancel", "gray1",
                                                {"midtop": (screen.centerx, 
                                                                  self.instruct_label.rect.bottom + 5)})                                      
    
    def startup(self, persistent):
        pg.mouse.set_visible(False)
        self.world = persistent["world"]
        self.elf = persistent["elf"]
        self.persist = persistent
        
    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                for build in [x for x in self.world.buildings if x.name != "Tree"]:
                    if build.rect.collidepoint(event.pos):
                        if build.max_workers > 0:
                            self.elf.assign_job(build, self.world)
                            #self.persist["message"] = "{} has been assigned to {}".format(self.elf.name, self.elf.job.name)
                            #self.persist["previous"] = "MANAGING"
                            #self.next = "MESSAGEWINDOW"
                            
                            self.done = True
                            break
            elif event.button == 3:
                self.next = "MANAGING"
                self.done = True
                
    def update(self, surface, keys):
        # map scrolling
        self.world.scroll(pg.mouse.get_pos())        
        self.draw(surface)
        
    def draw(self, surface):
        self.world.draw(surface)
        self.instruct_label.draw(surface)
        self.instruct_label2.draw(surface)
        surface.blit(self.cursor, pg.mouse.get_pos())