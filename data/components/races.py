from random import randint, choice
import itertools as it
import pygame as pg
from .. import prepare


class Fence(object):
    def __init__(self, lefttop):
        self.image = prepare.GFX["fence"]
        self.rect = self.image.get_rect(topleft=lefttop)
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Cloud(object):
    def __init__(self, lefttop):
        self.image = choice([prepare.GFX["cloud1"]])
        self.rect = self.image.get_rect(topleft=lefttop)
        self.pos = lefttop
        self.distance = randint(2, 3)
        
    def move(self, x_offset):
        self.pos = (self.pos[0] + (x_offset / float(self.distance)), self.pos[1])
        self.rect.topleft = self.pos
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
class Race(object):
    race_names = {6000: "Sprint",
                           10000: "Mid-Distance",
                           16000: "Marathon"}
    def __init__(self, racers, distance, player):
        self.screen_rect = pg.display.get_surface().get_rect()
        self.racers = racers
        self.distance = distance
        self.race_name = self.race_names[self.distance]
        self.player = player
        self.racing = True
        self.dist_travelled = 0
        self.track_rect = pg.Rect(0, self.screen_rect.bottom - 380,
                                             self.screen_rect.width, 400)
        self.grass_rect = pg.Rect(0, self.track_rect.top - 100,
                                              self.screen_rect.width, 100)
        self.sky_rect = pg.Rect(0, 0, self.screen_rect.width,
                                           self.grass_rect.top)
        self.fences  = [Fence((x * 32, self.track_rect.top - 12)) for
                              x in range(int((self.distance/32) + 10))]
        self.clouds = [Cloud((randint(10, self.distance), randint(0, 150))) for
                             i in range(int(self.distance/350))] 
        self.finish_rect = pg.Rect(self.distance, self.track_rect.top, 5,
        self.track_rect.height)
        self.map_scale = int(self.distance / (self.screen_rect.width - 300))
        self.map_rect = pg.Rect(270, 20, self.distance / self.map_scale, 100)
        self.mapline_rect = pg.Rect(self.map_rect.left + 
                                                  int(self.finish_rect.left / self.map_scale),
                                                  self.map_rect.top, 2, self.map_rect.height)
        for racer in self.racers:
            racer.rect.centery += self.track_rect.top
        self.results = []
        self.done = False
        self.ticks = 0
        
    def update(self):
        if self.racing:
            self.clouds = [x for x in self.clouds if x.rect.right >= 0]
            for racer in self.racers:
                racer.update(self)
            if self.racers:
                lead = max([x.rect.right for x in self.racers])
                if lead >= self.screen_rect.width - 200:
                    x_offset = -(lead - (self.screen_rect.width - 200))        
                    for item in it.chain(self.racers, self.fences):
                        item.rect.move_ip((x_offset, 0))
                    self.finish_rect.move_ip((x_offset, 0)) 
                    for cloud in self.clouds:
                        cloud.move(x_offset)
                    self.dist_travelled += -x_offset
            else:
                self.done = True
                self.racing = False                
        self.ticks += 1
            
    def draw(self, surface):
        surface.fill(pg.Color("black"))
        pg.draw.rect(surface, (73, 37, 25), self.track_rect)
        pg.draw.rect(surface, pg.Color(224, 255, 255), self.grass_rect)
        pg.draw.rect(surface, pg.Color("lightblue"), self.sky_rect)
        for cloud in sorted([x for x in self.clouds if x.rect.left <= self.screen_rect.right], reverse=True):
            cloud.draw(surface)
        pg.draw.rect(surface, (73, 37, 25), self.map_rect)
        pg.draw.rect(surface, pg.Color("white"), self.finish_rect)
        for fence in self.fences:
            fence.draw(surface)
        for deer in self.racers:
            surface.blit(deer.surface, deer.rect)
            pg.draw.rect(surface, pg.Color(deer.color), 
                               (deer.rect.left + deer.blanket_pos[0],
                               deer.rect.top + deer.blanket_pos[1],
                               7, 6))
            pg.draw.rect(surface, pg.Color("white"), self.mapline_rect)                   
            pg.draw.rect(surface, pg.Color(deer.color), 
                                (self.map_rect.left + int(deer.x_pos / self.map_scale),
                                self.map_rect.top + (10 * deer.num),
                                5, 5))
        top = 10
        ranked = sorted(self.racers, key=lambda x: x.x_pos, reverse=True)
        for winner in self.results:
            pg.draw.rect(surface, pg.Color(winner.color), (10, top, 10, 10))
            winner.name_label.rect.topleft = (25, top)
            winner.name_label.draw(surface)    
            top += 20
        if len(self.results) < 4:
            for racer in ranked[:4 - len(self.results)]:
                pg.draw.rect(surface, pg.Color(racer.color), (10, top, 10, 10))
                racer.name_label.rect.topleft = (25, top)
                racer.name_label.draw(surface)
                top += 20
            
            