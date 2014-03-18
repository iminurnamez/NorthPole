import sys
import random
import itertools as it
import json
import pygame as pg

from .obstacles import (Tree, LeftGate, RightGate, Jump, Rock, Pylon,
                                     UpChair, DownChair)



class Course(object):
    def __init__(self):
        self.obstacles = []
        self.jumps= []
        self.pylons = []
        self.upchairs = []
        self.downchairs = []

class CourseEditor(tools._State):
    def __init__(self):
        super(CourseEditor, self).__init__()
        self.next = 


    
def make_course(course_name, course_width, course_length, editing,
                             chairlift):
    pg.init()
    screen = pg.display.set_mode((width, height))
    screen_rect = screen.get_rect()
    clock = pg.time.Clock()
    course = Course()
    course_rect = pg.Rect(0, 0, course_width, course_length)
    start_rect = pg.Rect(course_rect.centerx - 8, 0, 20, 20)
    class_map = {"Tree": Tree,
                         "LeftGate": LeftGate,
                         "RightGate": RightGate,
                         "Jump": Jump,
                         "Rock": Rock,
                         "Pylon": Pylon,
                         "UpChair": UpChair,
                         "DownChair": DownChair}
    hazards = []
    pylons = []
    if editing:
        f = open(course_name, "r")
        obstacles = json.load(f)
        f.close() 
        for obstacle in obstacles:
            hazards.append(class_map[obstacle[0]]((obstacle[1][0],
                                     obstacle[1][1]), obst_images, course))       
    else:
        if chairlift:
            for i in range((course_length/164) - 2):
                pylon_lftp = ((course_width / 2) - 25, 200 + (i * 164))
                new_pylon = Pylon(pylon_lftp, obst_images, course)
                hazards.append(new_pylon)
                pylons.append(new_pylon)
        for j in range(int(course_length * course_width * .001)):
            x = random.randint(1, course_width - 17)
            y = random.randint(1, course_length - 33)
            check_rect = pg.Rect(x, y, 16, 32)
            if not [pylon for pylon in pylons if pylon.rect.colliderect(
                                                                                     check_rect)]:
                hazards.append(Tree((x, y), obst_images, course))           
            
    hazard_classes = it.cycle([Tree, LeftGate, RightGate, Jump, Pylon,
                                           Rock, None])
    current_hazard = next(hazard_classes)
    while True:
        info_label = Label(16, "{}  Current Obstacle: {}".format(
                                   course_name, current_hazard), "gray1",
                                   "bottomleft", 0, screen_rect.height,
                                   "lightgray")
                                   
        move_keys = {pg.K_LEFT: (64, 0),
                              pg.K_a: (64, 0),
                              pg.K_RIGHT: (-64, 0),
                              pg.K_d: (-64, 0),
                              pg.K_UP: (0, 64),
                              pg.K_w: (0, 64),
                              pg.K_DOWN: (0, -64),
                              pg.K_s: (0, -64)}
    
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_n:
                    current_hazard = next(hazard_classes)
                elif event.key == pg.K_SPACE:
                    for hazard in hazards:
                        hazard.rect.move_ip(-course_rect.left, -course_rect.top)
                    course_rect.move_ip(-course_rect.left, -course_rect.top)
                    obstacles = [(x.name, x.rect.topleft) for x in hazards]
                    with open(course_name, "w") as f:
                        f.write(json.dumps(obstacles))
                elif event.key == pg.K_i:
                    save_surface = pg.Surface((course.width, course.length))
                    save_surface.fill(pg.Color("white"))
                    course_rect.move_ip(-course_rect.left, -course_rect.top)
                    for hazard in hazards:
                        hazard.rect.move_ip(-course_rect.left, -course_rect.top)
                        hazard.display(save_surface)
                    pg.image.save(save_surface, course_name)                        
                
                if event.key in move_keys:
                    for item in hazards:
                        item.rect.move_ip(move_keys[event.key])
                    course_rect.move_ip(move_keys[event.key])
                    start_rect.move_ip(move_keys[event.key])
            elif event.type == pg.MOUSEBUTTONDOWN:
                if current_hazard:
                    new_hazard = current_hazard(event.pos, obst_images,
                                                                 course)
                    new_hazard.rect.bottomleft = event.pos
                    hazards.append(new_hazard)
                else:    
                    for hazard in [x for x in hazards if x.rect.colliderect(screen_rect)]:
                        if hazard.rect.collidepoint(event.pos):
                            hazards.remove(hazard)                        

        screen.fill(pg.Color("black"))
        pg.draw.rect(screen, pg.Color("white"), course_rect)
        pg.draw.rect(screen, pg.Color("blue"), start_rect)
        for hazard in hazards:
            hazard.display(screen)
        pg.draw.rect(screen,     
        pg.display.update()
        clock.tick(30)

def setup():
    affirmative = ["y", "yes", "Y", "Yes", "YES"]
    edit = raw_input("Create a new course?>")
    if edit in affirmative:
        editing = False
    else:
        editing = True
    filename = raw_input("Enter filename>")        
    length = int(raw_input("Enter course length>"))
    width = int(raw_input("Enter course width>"))
    chair = raw_input("Chairlift?>")
    if chair in affirmative:
        chairlift = True
    else:
        chairlift = False
    
    return filename, width, length, editing, chairlift
    
if __name__ == "__main__":
    make_course(setup())
    
    
#course1 = 16000 , 1920