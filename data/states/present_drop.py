from random import choice, randint
from itertools import chain
import pygame as pg
from .. import tools, prepare
from ..components.dropsleigh import DropSleigh, Colonial, Ranch, Gambrel, SmallHill, MediumHill, BigHill, Flat
from ..components.labels import Label


class Star(object):
    twinkle = pg.Surface((4, 4)).convert_alpha()
    twinkle.fill(pg.Color("yellow"))
    twinkle.set_alpha(64)
    
    def __init__(self, pos):
        self.pos = pos
        self.ticks = randint(0, 4)
        self.frequency = randint(10, 20)
        
    def update(self):
        self.ticks += 1
        self.twinkling = False
        if not self.ticks % self.frequency:
            self.twinkling = True
 
    def move(self, offset):
        self.pos = (self.pos[0] + (offset[0] / 2.0), self.pos[1])
        
    def draw(self, surface):
        twinkler = pg.Rect(self.pos, (2, 2))
        if self.twinkling:
            surface.blit(self.twinkle, (twinkler.left - 1, twinkler.top - 1))
            #pg.draw.rect(surface, (255, 255, 0, 255), twinkler)
        pg.draw.rect(surface, (255, 255, 0), twinkler)
        
        
class PresentDrop(tools._State):
    def __init__(self):
        super(PresentDrop, self).__init__()
        self.next = "MANAGING"
        self.screen_rect = pg.display.get_surface().get_rect()
        self.font = prepare.FONTS["weblysleekuil"]
        
    def startup(self, persistent):
        self.persist = persistent    
           
        self.sleigh = DropSleigh((300, 300))
        self.hills = [SmallHill((1000, 650)), BigHill((5000, 500)), MediumHill((8000, 600))]
        self.flats = [Flat((3000, 730)), Flat((9400, 720)), Flat((4000, 720))]
        self.gifts = []
        self.stars = [Star((randint(1, self.screen_rect.right), randint(1, self.screen_rect.bottom - 150)))
                           for _ in range(50)]
        
        self.snow_rect = pg.Rect(0, self.screen_rect.bottom - 60,
                                             self.screen_rect.width, 60)
        self.offset = 0.0
        self.gifts_delivered = 0
        self.gifts_dropped = 0
        self.time_elapsed = 0
        
        
    def get_event(self, event):
        if event.type == pg.QUIT:
            self.done = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.done = True
            elif event.key == pg.K_SPACE:
                if self.sleigh.launch_gift(self.gifts):
                    self.gifts_dropped += 1

    def move(self, offset):
        for hill in self.hills:
            hill.move(offset)
        for flat in self.flats:
            flat.move(offset)
        for gift in self.gifts:
            gift.move(offset)
        

    def update(self, surface, keys):
        self.time_elapsed += 1/float(self.fps)
        if len(self.stars) < 50:
            self.stars.append(Star((self.screen_rect.right + 3,
                                               randint(1, self.screen_rect.bottom - 150))))
        x_velocity = self.sleigh.update(keys)
        
        
        for star in self.stars:
            star.update()
        self.offset += x_velocity
        self.move((-x_velocity, 0)) 
        for star in self.stars:
            star.move((-x_velocity, 0))
        self.stars = [x for x in self.stars if x.pos[0] > -3]
        for gift in self.gifts:
            gift.update(chain(self.hills, self.flats), self.snow_rect)
        self.gifts_delivered += len([g for g in self.gifts if g.delivered])    
        
        self.gifts = [x for x in self.gifts if not x.done and not x.delivered]
        self.dropped_label = Label(self.font, 24, "Gifts Dropped: {}".format(self.gifts_dropped),
                                                "white", {"topleft": (5, 5)})
        self.delivered_label = Label(self.font, 24, "Gifts Delivered: {}".format(self.gifts_delivered),
                                                 "white", {"top": self.dropped_label.rect.bottom + 5,
                                                               "left": self.dropped_label.rect.left})
        self.time_label = Label(self.font, 32, "{}".format(int(self.time_elapsed)),
                                          "white", {"topright": (self.screen_rect.right - 10, 10)})
        
        self.draw(surface)

    def draw(self, surface):
        surface.fill(pg.Color(0, 0, 64, 255))
        for star in self.stars:
            star.draw(surface)
        pg.draw.rect(surface, pg.Color("gray96"), self.snow_rect)
        for hill in self.hills:
            hill.draw(surface)
        for flat in self.flats:
            flat.draw(surface)
        self.sleigh.draw(surface)
        for gift in self.gifts:
            gift.draw(surface)
        self.dropped_label.draw(surface)
        self.delivered_label.draw(surface)
        self.time_label.draw(surface)