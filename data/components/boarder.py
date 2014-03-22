import itertools as it
import pygame as pg
from .. import prepare


class Boarder(object):
    def __init__(self, lefttop):
        screen_rect = pg.display.get_surface().get_rect()
        self.left_margin = screen_rect.width / 3
        self.right_margin = (screen_rect.width / 3) * 2
        self.y_margin = screen_rect.height / 2
        self.speed = 4
        self.direction = "down"
        self.turned = False
        self.jumping = False
        self.grabbing = False
        self.jump_count = 0
        self.x_velocity = 0
        self.y_velocity = 0
        self.image_dict = {
                    "brake": {"left": it.cycle([prepare.GFX["leftboardbrake1"],
                                                          prepare.GFX["leftboardbrake2"],
                                                          prepare.GFX["leftboardbrake3"]]),                                
                                   "right": it.cycle([prepare.GFX["rightboardbrake1"],
                                                            prepare.GFX["rightboardbrake2"],
                                                            prepare.GFX["rightboardbrake3"]]),
                                   "down": it.cycle([prepare.GFX["downboardbrake1"]])},
                    "no brake": {"left": it.cycle([prepare.GFX["leftboard1"],
                                                              prepare.GFX["leftboard2"],
                                                              prepare.GFX["leftboard3"]]),                                
                                       "right": it.cycle([prepare.GFX["rightboard1"],
                                                                prepare.GFX["rightboard2"],
                                                                prepare.GFX["rightboard3"]]),
                                       "down": it.cycle([prepare.GFX["downboard1"],
                                                                 prepare.GFX["downboard2"],
                                                                 prepare.GFX["downboard3"]])},
                    "grab": {"left": it.cycle([prepare.GFX["leftgrab"]]),
                                 "right": it.cycle([prepare.GFX["rightgrab"]]),
                                 "down": it.cycle([prepare.GFX["downgrab"]]),
                                 "up": it.cycle([prepare.GFX["upgrab"]])},
                    "no grab": {"left": it.cycle([prepare.GFX["leftjump"]]),                                
                                      "right": it.cycle([prepare.GFX["rightjump"]]),
                                      "down": it.cycle([prepare.GFX["downjump"]]),
                                      "up": it.cycle([prepare.GFX["upjump"]])},
                    "crash": {"down": it.cycle([prepare.GFX["crash1"],
                                                            prepare.GFX["crash2"],
                                                            prepare.GFX["crash3"],
                                                            prepare.GFX["crash4"],
                                                            prepare.GFX["crash5"]])}}
        
        self.images = self.image_dict["no brake"][self.direction]
        self.image = next(self.images)
        self.rect = self.image.get_rect(topleft=lefttop)
        self.sized_rect = None
        self.spray_images = it.cycle([prepare.GFX["spray1"],
                                                  prepare.GFX["spray2"],
                                                  prepare.GFX["spray3"]])
        self.spray_image = next(self.spray_images)
        self.spray_rect = self.spray_image.get_rect()
        self.xpos = self.rect.left
        self.ypos = self.rect.top
        self.zpos = 0
        self.crashed = False
        self.crash_count = 0
        self.jump_history = ""
        self.acceleration = {"left": False,
                                     "right": False,
                                     "down": False,
                                     "braking": False}
        self.grunt = prepare.SFX["elfgrunt"]
        self.glide = prepare.SFX["edgegrind"]
        self.glide.set_volume(.1)

    def control(self, keys):
        last_direction = self.direction
        accels = {pg.K_LEFT: "left",
                       pg.K_RIGHT: "right",
                       pg.K_DOWN: "down",
                       pg.K_SPACE: "braking"}
        if keys[pg.K_SPACE]:
            glide_channel = pg.mixer.Channel(1)
            glide_channel.play(self.glide)
        else:
            self.glide.stop()
        for key in accels:
            if keys[key]:
                self.acceleration[accels[key]] = True
            else:
                self.acceleration[accels[key]] = False
        self.turned = True
        if self.acceleration["down"]:
            self.direction = "down"
        elif self.acceleration["left"]:
            self.direction = "left"
        elif self.acceleration["right"]:
            self.direction = "right"
            
        if self.direction != last_direction:
            self.turned = True
            
    def crash(self, crash_count):
        if not self.crashed:
            self.grunt.play()
            self.crashed = True
            self.crash_count = crash_count
            self.x_velocity = -self.x_velocity / 2.0
            self.y_velocity = 1
            for key in self.acceleration:
                self.acceleration[key] = False
            
        
    def recover(self):
        self.crashed = False 
        self.x_velocity = 0
        self.y_velocity = 0
        self.direction = "left"
        
    def jump(self, jump_count):      
        self.jumping = True
        self.acceleration["braking"] = False
        self.turned = True
        self.direction = "down"
        self.jump_count = jump_count
        self.x_velocity = 0
        self.y_velocity = 0
        self.zpos = -1
    
    def judge_tricks(self):
        trick_map = {"downleftuprightdownleftuprightdown": "720",
                             "downrightupleftdownrightupleftdown": "720",
                             "downleftuprightdown": "360", 
                             "downrightupleftdown": "360"}
        tricks = {"720": 0,
                      "360": 0}
        for key in trick_map:
            tricks[trick_map[key]] += self.jump_history.count(key)
        tricks["360"] -= tricks["720"]
        print tricks
        self.jump_history = ""
    
    def update_image(self):    
        if self.crashed:
            self.images = self.image_dict["crash"]["down"]
        
        elif self.acceleration["braking"]:
            if self.acceleration["down"]:
                self.images = self.image_dict["brake"]["down"]
            else:
                self.images = self.image_dict["brake"][self.direction]
                self.spray_image = next(self.spray_images)
       
        elif self.jumping:
            if self.grabbing:
                self.images = self.image_dict["grab"][self.direction]
            else:
                self.images = self.image_dict["no grab"][self.direction]
        
        else:
            self.images = self.image_dict["no brake"][self.direction]
        self.image = next(self.images)
            
    def update(self, ticks, course, keys):
        if self.jumping:
            for key in self.acceleration:
                self.acceleration[key] = False
            if self.jump_count > 0:
                self.zpos -= 1
            elif self.zpos < 0:
                self.zpos += 1
            if self.zpos >= 0:
                self.jumping = False
                self.jump_count = 0
                self.y_velocity = self.speed
                if self.direction != "down":
                    self.crashed = True
                    self.crash_count = 45
                    self.direction = "down"
                else:
                    self.judge_tricks()
            self.jump_count -= 1
        elif self.crashed:
            if self.crash_count > 0:
                self.crash_count -= 1
                if self.x_velocity < 0:
                    self.x_velocity += .01
                elif self.x_velocity > 0:
                    self.x_velocity -= .01
            else:
                self.recover()
        else:
            self.control(keys)        
        if self.acceleration["left"]:
            self.x_velocity -= .1
            self.y_velocity -= .005
        if self.acceleration["right"]:
            self.x_velocity += .1
            self.y_velocity -= .005
        if self.acceleration["down"]:
            self.y_velocity += .1
            if self.x_velocity < 0:
                self.x_velocity += .05
            elif self.x_velocity > 0:
                self.x_velocity -= .05            
        if self.acceleration["braking"]:
            if self.x_velocity < 0:
                self.x_velocity += .025
            elif self.x_velocity > 0:
                self.x_velocity -= .025
            self.y_velocity -= .05
        if self.x_velocity < -self.speed:
            self.x_velocity = -self.speed
        elif self.x_velocity > self.speed:
            self.x_velocity = self.speed
        if self.y_velocity < 0:
            self.y_velocity = 0
        elif self.y_velocity > self.speed:
            self.y_velocity = self.speed
        self.xpos += self.x_velocity
        self.ypos += self.y_velocity
        
        
        offset = (0, 0)
        if self.ypos <= self.y_margin:
            self.rect.top =  int(self.ypos)
        else:
            offset = (offset[0], offset[1] + int(-self.y_velocity))
            self.ypos += int(-self.y_velocity)
        if self.xpos <= self.left_margin or self.xpos >= self.right_margin:
            offset = (offset[0] + int(-self.x_velocity), offset[1])
            self.xpos += int(-self.x_velocity)
        else:
            self.rect.left = int(self.xpos)
        if offset[0] or offset[1]:
            course.move(offset)
        if self.turned:
            self.update_image()
        else:
            if not ticks % 10:
                self.image = next(self.images)

        
            
    def display(self, surface):
        zrect = self.rect.move((0, int(self.zpos)))
        if self.zpos < 0:
            size = (-self.zpos/12) * 2
            sized_rect = zrect.inflate(size, size)
            sized = pg.transform.scale(self.image, sized_rect.size)
            surface.blit(sized, sized_rect)
        else:    
            surface.blit(self.image, zrect)
        
        if self.acceleration["braking"] and [x for x in [self.x_velocity,
                                                            self.y_velocity] if x != 0]:
            self.spray_rect.midbottom = (self.rect.centerx,
                                                        self.rect.bottom + 3)
            surface.blit(self.spray_image, self.spray_rect)