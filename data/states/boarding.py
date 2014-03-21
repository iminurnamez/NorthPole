import os
import json
import pygame as pg

from .. import prepare, tools
from ..components import course
from ..components import obstacles
from ..components import boarder


class Boarding(tools._State):
    def __init__(self):
        tools._State.__init__(self)
        self.next = "MANAGING"
        self.clock = pg.time.Clock()
        self.fps = 60
        self.ticks = 1
        
        with open(os.path.join("resources", "mtkringle.json"), "r") as f:
            course_items = json.load(f)
        self.course = course.Course(1920, 16000, course_items)        
        self.boarder = boarder.Boarder(
                              (pg.display.get_surface().get_width() / 2, 0))
        
    def startup(self, persistant):
        self.__init__()
        self.player = persistant["player"] 
        pg.mouse.set_visible(False)
        return tools._State.startup(self, persistant)
        
    def cleanup(self):
        pg.mouse.set_visible(True)
        self.persist["player"] = self.player
        self.done = False
        return tools._State.cleanup(self)
        
    def update(self, surface, keys):
        self.boarder.update(self.ticks, self.course, keys)
        self.course.update(self.boarder, surface.get_rect(), self.ticks)
        
        if self.boarder.rect.colliderect(self.course.bottom_lifthut.rect):
            #TODO: update player stats
            self.next = "BOARDING"
            self.done = True
        if (self.boarder.rect.bottom > 
                        self.course.bottom_lifthut.rect.bottom + 100):
            #TODO: update player stats
            self.done = True        
        surface.fill(pg.Color("white"))
        self.course.display(surface, self.boarder)
        self.ticks += 1
        
    def get_event(self, event):
        jump_map = {pg.K_DOWN: "down",
                              pg.K_UP: "up",
                              pg.K_LEFT: "left",
                              pg.K_RIGHT: "right"}
        opposites = {pg.K_DOWN: "up",
                            pg.K_UP: "down",
                            pg.K_LEFT: "right",
                            pg.K_RIGHT: "left"}
        
        if event.type == pg.QUIT:
            return False 
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.done = True
            elif self.boarder.jumping:
                try:
                    if self.boarder.direction != opposites[event.key]:    
                        self.boarder.direction = jump_map[event.key]
                        self.boarder.turned = True
                        self.boarder.jump_history += self.boarder.direction
                except KeyError:
                    pass
                if event.key == pg.K_SPACE:
                    self.boarder.grabbing = True   
        elif event.type == pg.KEYUP:
            if self.boarder.jumping:
                    if event.key == pg.K_SPACE:
                        self.boarder.grabbing = False                    
            elif event.key == pg.K_SPACE and not self.boarder.crashed:
                self.boarder.glide.stop()        
