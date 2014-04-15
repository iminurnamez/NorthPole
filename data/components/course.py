import itertools as it
import pygame as pg
from obstacles import (Tree, RightGate, LeftGate, Jump, Rock, Pylon, UpChair, 
                                    DownChair, TopLiftHut, BottomLiftHut)

class Course(object):
    def __init__(self, obstacle_list):
        screen_rect = pg.display.get_surface().get_rect()
        class_map = {"tree": Tree,
                             "rightgate": RightGate,
                             "leftgate": LeftGate,
                             "jump": Jump,
                             "rock": Rock,
                             "pylon": Pylon,
                             "upchair": UpChair,
                             "downchair": DownChair,
                             "toplifthut": TopLiftHut,
                             "bottomlifthut": BottomLiftHut}

        self.obstacles = []
        self.jumps = []
        self.pylons = []
        self.upchairs = []
        self.downchairs = []
        
        for item in obstacle_list:
            if item[0] == "Width":
                self.width = item[1]
            elif item[0] == "Length":
                self.length = item[1]
            else:
                obstacle = class_map[item[0].lower()]((item[1][0] - ((self.width/2) - (screen_rect.width / 2)), item[1][1]), self)            
        if self.pylons:
            hutleft = self.pylons[0].rect.left + 2
        else:
            hutleft = -500 #keep the huts offscreen if there's no chairlift 
        self.top_fourth = [x for x in self.obstacles if x.rect.bottom <= (self.length / 4)]
        self.second_fourth = [x for x in self.obstacles if self.length / 4 < x.rect.bottom <= (self.length / 4) * 2]
        self.third_fourth = [x for x in self.obstacles if (self.length / 4) * 2 < x.rect.bottom <= (self.length / 4) * 3]
        self.bottom_fourth = [x for x in self.obstacles if (self.length / 4) * 3 < x.rect.bottom <= self.length]
        self.obstacles = [x for x in self.top_fourth]
        self.second_added = False        
        self.third_added = False
        self.fourth_added = False
        self.total_offset = (0, 0)
        self.top_lifthut = TopLiftHut((hutleft, 145), self)
        self.bottom_lifthut = BottomLiftHut((hutleft, self.length - 248), self)
        if self.pylons:
            half_width = self.pylons[0].rect.centerx 
            for i in range(len(self.pylons) / 2):
                uchair = UpChair((half_width + 18, 260 + (i * 328)), self)
                dchair = DownChair((half_width - 31, 320 + (i * 328)), self)

        
        self.ticks = 1
        
    def move(self, offset):
        self.total_offset = (self.total_offset[0] + offset[0],
                                    self.total_offset[1] + offset[1])
        for item in it.chain(self.jumps, self.obstacles, self.pylons,
                                     self.upchairs, self.downchairs):
            item.move(offset)

    def update(self, boarder, screen_rect, ticks):
        if not self.second_added and self.total_offset[1] - 1000 < -self.length/4:
            for second in self.second_fourth:
                second.rect.move_ip(self.total_offset)
                second.collision_rect.move_ip(self.total_offset)
            self.obstacles.extend(self.second_fourth)
            self.second_fourth = []
            self.second_added = True
            
        elif not self.third_added and self.total_offset[1] - 1000 < (-self.length/4) * 2:
            for third in self.third_fourth:
                third.rect.move_ip(self.total_offset)
                third.collision_rect.move_ip(self.total_offset)
            self.obstacles.extend(self.third_fourth)
            self.third_fourth = []
            self.third_added = True
        elif not self.fourth_added and self.total_offset[1] - 1000 < (-self.length/4) * 3:
            for fourth in self.bottom_fourth:
                fourth.rect.move_ip(self.total_offset)
                fourth.collision_rect.move_ip(self.total_offset)
            self.obstacles.extend(self.bottom_fourth)
            self.bottom_fourth = []
            self.fourth_added = True
        self.obstacles = [x for x in self.obstacles if x.rect.bottom > 0]
        self.pylons = [x for x in self.pylons if x.rect.bottom > 0]
        self.jumps = [x for x in self.jumps if x.rect.bottom > 0]
        self.upchairs = [x for x in self.upchairs if x.rect.top > self.top_lifthut.rect.bottom]
        self.downchairs = [x for x in self.downchairs if x.rect.bottom < self.bottom_lifthut.rect.bottom]
        all_items = list(it.chain(self.obstacles, self.jumps, self.pylons,
                                           self.upchairs, self.downchairs))
        on_screen = set([x for x in all_items if (
                                             x.rect.top < screen_rect.height and
                                             x.rect.right > 0 and 
                                             x.rect.left < screen_rect.width)]) 
        if self.pylons:
            half_width = self.pylons[0].rect.centerx
            if len(self.upchairs) < len(self.pylons) / 2:
                new_uchair = UpChair((half_width + 18, self.bottom_lifthut.rect.top - 5), self)
            if len(self.downchairs) < len(self.pylons) / 2:
                new_dchair = DownChair((half_width - 31, self.top_lifthut.rect.bottom + 5), self)
        for obstacle in it.chain(self.jumps, self.obstacles, self.upchairs,
                                           self.downchairs, self.pylons):
            obstacle.update(boarder)
            if (obstacle in on_screen and 
                            obstacle.collision_rect.colliderect(boarder.rect)):
                obstacle.collide_with_boarder(boarder)                 
       
    def display(self, surface, snowboarder):
        screen_bottom = surface.get_height()
        viewable_jumps = [x for x in self.jumps if x.rect.top < screen_bottom]
        for jump in viewable_jumps:
            jump.display(surface)
        snowboarder.display(surface)
        viewable = [x for x in self.obstacles if x.rect.top < screen_bottom]
        for item in viewable:
            item.display(surface)
        for chair in it.chain(self.pylons, self.upchairs, self.downchairs):
            chair.display(surface)        
        if self.pylons:
            for hut in [self.top_lifthut, self.bottom_lifthut]:
                hut.display(surface)

