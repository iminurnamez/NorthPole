import pygame as pg
from .. import tools, prepare


class ElfAssignment(tools._State):
    def __init__(self):
        super(ElfAssignment, self).__init__()
        self.cursor = prepare.GFX["canecursor"]
        self.next = "MANAGING"
        
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
                            self.elf.assign_job(build)
                            self.persist["message"] = "{} has been assigned to {}".format(self.elf.name, self.elf.job.name)
                            self.persist["previous"] = "MANAGING"
                            self.next = "MESSAGEWINDOW"
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
        surface.blit(self.cursor, pg.mouse.get_pos())