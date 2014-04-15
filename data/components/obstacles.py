import random
import pygame as pg
from .. import prepare, tools

      
class Obstacle(object):
    def __init__(self, name, lefttop, collider_tl, collider_size):
        self.name = name
        self.image = prepare.GFX[self.name]
        self.pos = lefttop
        self.rect = self.image.get_rect(topleft=lefttop)
        self.collidex = collider_tl[0]
        self.collidey = collider_tl[1]
        self.collision_rect = pg.Rect((self.rect.left + self.collidex,
                                                  self.rect.top + self.collidey),
                                                  collider_size)
            
    def move(self, offset):
        self.rect.move_ip(offset)
        self.collision_rect.move_ip(offset)
        
    def collide_with_boarder(self, boarder):
        pass
    
    def update(self, boarder):
        pass
       
    def display(self, surface):
        surface.blit(self.image, self.rect)
        

class Tree(Obstacle):
    def __init__(self, lefttop, course):
        super(Tree, self).__init__("tree", lefttop, (11, 27), (3, 4))
        course.obstacles.append(self)
    
    def collide_with_boarder(self, boarder):
        boarder.crash(45)
    
class Rock(Obstacle):
    def __init__(self, lefttop, course):
        super(Rock, self).__init__("rock", lefttop, (0, 24), (23, 8))
        course.obstacles.append(self)
    
    def collide_with_boarder(self, boarder):
        boarder.crash(45)
        
    
class LeftGate(Obstacle):
    def __init__(self, lefttop, course):
        super(LeftGate, self).__init__("leftgate", lefttop, (16, 32), (6, 6))
        self.passed_image = prepare.GFX["passedgate"]
        self.passed = False
        self.sound = prepare.SFX["boing1"]
        course.obstacles.append(self)
        
    def update(self, boarder):
        if not self.passed: 
            if self.collision_rect.top <= boarder.rect.centery <= self.rect.bottom:
                if self.rect.left - 150 <= boarder.rect.centerx <= self.collision_rect.left:
                    self.image = self.passed_image
                    self.sound.play()
                self.passed = True
            
    def collide_with_boarder(self, boarder):
        pass
        
        
class RightGate(Obstacle):
    def __init__(self, lefttop, course):
        super(RightGate, self).__init__("rightgate", lefttop, (16, 32), (6, 6))
        self.passed_image = prepare.GFX["passedgate"]
        self.passed = False
        self.sound = prepare.SFX["boing2"]
        course.obstacles.append(self)
        
    def update(self, boarder):
        if not self.passed: 
            if self.collision_rect.top <= boarder.rect.centery <= self.rect.bottom:
                if self.collision_rect.right + 150 >= boarder.rect.centerx >= self.collision_rect.right:
                    self.image = self.passed_image
                    self.sound.play()
                self.passed = True
        
class Jump(Obstacle):
    def __init__(self, lefttop, course):
        self.entrance = "down"
        super(Jump, self).__init__("jump", lefttop, (0, 6), (29, 15))
        self.hit = False
        course.jumps.append(self)
        
    def collide_with_boarder(self, boarder):
        if not self.hit:
            self.hit = True
            if boarder.direction == self.entrance:
                boarder.jump(int(15 * boarder.y_velocity))
            else:
                boarder.crash(45)
            
         
class Chair(object):
    def __init__(self, name, lefttop, y_velocity):
        self.name = name
        self.pos = lefttop
        self.y_velocity = y_velocity
        self.image = prepare.GFX[self.name]
        self.rect = self.image.get_rect(topleft=lefttop)
        self.collision_rect = pg.Rect(self.rect.center, (2, 2))
        self.collidex = 0
        self.collidey = 0
        

    def move(self, offset):
        self.rect.move_ip(offset)
        self.collision_rect.move_ip(offset)
    
    def collide_with_boarder(self, boarder):
        pass    
    
    def update(self, boarder):
        self.move((0, self.y_velocity))
        
    def display(self, surface):
        surface.blit(self.image, self.rect)
       
class DownChair(Chair):
    def __init__(self, lefttop, course):
        super(DownChair, self).__init__("downchair", lefttop, 1)
        course.downchairs.append(self)
        
class UpChair(Chair):
    def __init__(self, lefttop, course):
        super(UpChair, self).__init__("upchair", lefttop, -1)
        if random.randint(0, 1):
            self.image = prepare.GFX["upchairfull"]
        course.upchairs.append(self)
        
class TopLiftHut(Obstacle):
    def __init__(self, lefttop, course):
        super(TopLiftHut, self).__init__("toplifthut", lefttop, (0, 0), (2, 2))
        course.obstacles.append(self)
        
class BottomLiftHut(Obstacle):
    def __init__(self, lefttop, course):
        super(BottomLiftHut, self).__init__("bottomlifthut", lefttop, (0, 0), (2, 2))
        course.obstacles.append(self)

class Pylon(Obstacle):
    def __init__(self, lefttop, course):
        super(Pylon, self).__init__("pylon", lefttop, (23, 90), (4, 5))
        course.pylons.append(self)
        
    def collide_with_boarder(self, boarder):
        boarder.crash(45)    
        
        
class FinishLine(object):
    def __init__(self, lefttop, line_width):
        self.image = prepare.GFX["finishline"]
        self.rect = self.image.get_rect(topleft=lefttop)         
        
    def collide_with_boarder(self, boarder):
        pass 
        
        
class DiscBasket(Obstacle):
    def __init__(self, lefttop, course):
        super(DiscBasket, self).__init__("discbasket", lefttop, (6, 4), (21, 16))
        course.basket = self
        course.obstacles.append(self)

class TeeBox(object):
    def __init__(self, lefttop, course):
        self.image = prepare.GFX["teebox"]
        self.rect = self.image.get_rect(topleft=lefttop)
        course.teebox = self
        
        