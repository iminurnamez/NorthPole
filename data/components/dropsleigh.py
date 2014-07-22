from math import radians, sin, cos
from random import choice, randint
from itertools import cycle, chain
import pygame as pg
from .. import prepare


class Gift(object):
    images = ["gift1"]
    
    def __init__(self, center_point):
        self.image = prepare.GFX[choice(self.images)]
        self.rect = self.image.get_rect(center=center_point)
        self.pos = self.rect.topleft
        self.velocity = (0, 0)
        self.done = False
        self.delivered = False
        
    def update(self, hoods, snow_rect):
        self.pos = (self.pos[0] + self.velocity[0],
                         self.pos[1] + self.velocity[1])
        self.rect.center = self.pos
        self.velocity = (self.velocity[0] - .005, self.velocity[1] + .03)
        if snow_rect.colliderect(self.rect):
            self.done = True
            return
        for house_list in chain([hood.houses for hood in hoods]):
            for house in house_list:
                if house.cap_rect.colliderect(self.rect):
                    self.delivered = True
                    break
                elif (house.house_rect.colliderect(self.rect)
                       or house.chimney_rect.colliderect(self.rect)):
                    self.done = True
                    break
   
    def move(self, offset):
        self.pos = (self.pos[0] + offset[0],
                         self.pos[1] + offset[1])
        self.rect.center = self.pos 

    def draw(self, surface):
        surface.blit(self.image, self.rect)

        
class House(object):
    def __init__(self, center_bottom, img_name, house_info, chimney_info, cap_info):
        self.image = prepare.GFX[img_name]
        self.rect = self.image.get_rect(midbottom=center_bottom)
        self.pos = self.rect.topleft
        self.house_info = house_info
        self.chimney_info = chimney_info
        self.cap_info = cap_info
        self.house_rect = pg.Rect((self.rect.left + self.house_info[0],
                                               self.rect.top + self.house_info[1]),
                                               self.house_info[2])
        self.chimney_rect = pg.Rect((self.rect.left + self.chimney_info[0],
                                                   self.rect.top + self.chimney_info[1]),
                                                   self.house_info[2])
        self.cap_rect = pg.Rect((self.rect.left + self.cap_info[0],
                                            self.rect.top + self.cap_info[1]),
                                            self.house_info[2])
        
    def move(self, offset):
        self.pos = (self.pos[0] + offset[0],
                         self.pos[1] + offset[1])
        self.rect.topleft = self.pos
        self.house_rect = pg.Rect((self.rect.left + self.house_info[0],
                                               self.rect.top + self.house_info[1]),
                                               self.house_info[2])
        self.chimney_rect = pg.Rect((self.rect.left + self.chimney_info[0],
                                                   self.rect.top + self.chimney_info[1]),
                                                   self.chimney_info[2])
        self.cap_rect = pg.Rect((self.rect.left + self.cap_info[0],
                                            self.rect.top + self.cap_info[1]),
                                            self.cap_info[2])
    
    def draw(self, surface):
        surface.blit(self.image, self.pos)        
        

class Colonial(House):
    img_names = ["colonial", "colonial2"]
    def __init__(self, center_bottom):
        super(Colonial, self).__init__(center_bottom, choice(self.img_names),
                                                   (7, 85, (114, 111)), (76, 50, (20, 37)),
                                                   (75, 47, (22, 3)))

        
class Ranch(House):
    img_names = ["ranch", "ranch2", "ranch3"]
    def __init__(self, center_bottom):
        super(Ranch, self).__init__(center_bottom, choice(self.img_names),
                                                 (2, 32, (123, 64)), (79, 10, (20, 22)),
                                                 (78, 7, (22, 3)))


class Gambrel(House):
    img_names = ["gambrel", "gambrel2"]
    def __init__(self, center_bottom):
        super(Gambrel, self).__init__(center_bottom, choice(self.img_names),
                                                    (8, 39, (78, 73)), (53, 4, (20, 37)),
                                                    (52, 1, (22, 3)))


class Hill(object):
    def __init__(self, center_top, radius, angles):
        self.pos = (center_top[0], center_top[1] + radius)
        self.radius = radius
        self.houses = []
        for angle in angles:
            dist = (self.radius - 20) - (abs(90 - angle) / 2)
            mb = (int(self.pos[0] + (cos(radians(angle)) * dist)),
                      int(self.pos[1] - (sin(radians(angle)) * dist)))
            self.houses.append(choice([Colonial, Ranch, Gambrel])(mb))                      
      
    def draw(self, surface):
        pg.draw.circle(surface, pg.Color("gray96"), (int(self.pos[0]), int(self.pos[1])), self.radius)
        for house in self.houses:
            house.draw(surface)
            
    def move(self, offset):
        self.pos = (self.pos[0] + offset[0],
                        self.pos[1] + offset[1])
        for house in self.houses:
            house.move(offset)
            
            
class BigHill(Hill):
    def __init__(self, center_top):
        super(BigHill, self).__init__(center_top, 2500, [70, 75, 80, 85, 90, 95, 100, 105, 110])

        
class MediumHill(Hill):
    def __init__(self, center_top):
        super(MediumHill, self).__init__(center_top, 2000, [78, 84, 90, 96, 102])

        
class SmallHill(Hill):
   def __init__(self, center_top):
        super(SmallHill, self).__init__(center_top, 1500, [84, 90, 96])
        
        
class Flat(object):
    def __init__(self, center_bottom):
        self.rect = pg.Rect(0, 0, 2000, 256)
        self.rect.midbottom = center_bottom
        left = center_bottom[0] - 1000
        self.houses = []
        for i in range(1, 6):    
            self.houses.append(choice([Colonial, Ranch, Gambrel])((left + (200 * i), center_bottom[1] - randint(5, 25))))
            
    def move(self, offset):
        for house in self.houses:
            house.move(offset)
            
    def draw(self, surface):
        for house in self.houses:
            house.draw(surface)
            
            
class DropSleigh(object):
    front_reins = prepare.GFX["reins"]
    back_reins = prepare.GFX["backreins"]
    
    def __init__(self, lefttop):
        self.sleigh_image = prepare.GFX["sleigh"]
        self.dropper = prepare.GFX["dropper"]
        deer1 = pg.transform.flip(prepare.GFX["rightreindeer1"], True, False)
        deer2 =  pg.transform.flip(prepare.GFX["rightreindeer2"], True, False)
        self.reindeer_images = cycle([deer1, deer2])
        self.reindeer_image = next(self.reindeer_images)
        self.surface = pg.Surface(self.sleigh_image.get_size()).convert()
        self.surface.set_colorkey(pg.Color("black"))
        self.rect = self.surface.get_rect(topleft=lefttop)
        self.screen_rect = pg.display.get_surface().get_rect()
        self.x_velocity = 1.0
        self.max_velocity = 4.0
        self.accel = .015
        self.y_pos = lefttop[1]
        self.state = "Ready"
        self.delay = 0
        self.gift = Gift((self.rect.left + 8, self.rect.top + 15))
        self.ticks = 0
        
    def update(self, keys):
        self.ticks += 1
        screen = self.screen_rect
        if keys[pg.K_DOWN] and self.rect.bottom < screen.bottom - 20:
            self.y_pos += 1.5
        if keys[pg.K_UP] and self.rect.top > 20:
            self.y_pos -= 1.5
        if keys[pg.K_LEFT] and (self.x_velocity > 1.5):
            self.x_velocity -= self.accel
        if keys[pg.K_RIGHT] and self.x_velocity < self.max_velocity:        
            self.x_velocity += self.accel

        self.rect.topleft = (self.rect.left, self.y_pos)
        self.rect.top = max(10, self.rect.top)
        self.rect.bottom = min(self.screen_rect.bottom - 20, self.rect.bottom)
            
        if self.state == "Loading":
            if self.delay:
                self.delay -= 1
            else:
                self.state = "Ready"
                self.gift = Gift((self.rect.left + 6, self.rect.top + 15))
        elif self.state == "Ready":
            self.gift.rect.center = (self.rect.left + 6, self.rect.top + 15)
            self.gift.pos = self.gift.rect.center
        if not self.ticks % int(10 - self.x_velocity):       
            self.reindeer_image = next(self.reindeer_images)
        return self.x_velocity
        
    def launch_gift(self, gifts):
        if self.state == "Ready":
            self.gift.velocity = (self.x_velocity, 1)
            gifts.append(self.gift)
            self.gift = None
            self.state = "Loading"
            self.delay = 45
            return True
        return False
        
    def move(self, offset):
        pass
        
        
    def draw(self, surface):
        self.surface.fill(pg.Color("black"))
        for tl in [(0, 12), (22, 12), (44, 12), (66, 12)]:
            self.surface.blit(self.reindeer_image, tl)
        self.surface.blit(self.back_reins, (9, 10))
        self.surface.blit(self.sleigh_image, (0, 0))
        self.surface.blit(self.dropper, (120, 0))
        for _tl in [(0, 16), (22, 16), (44, 16), (66, 16)]:
            self.surface.blit(self.reindeer_image, _tl)
        self.surface.blit(self.front_reins, (9, 14))
        self.surface = pg.transform.flip(self.surface, True, False)
        surface.blit(self.surface, self.rect)
        if self.gift:
            self.gift.draw(surface)
        