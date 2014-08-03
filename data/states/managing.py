import sys
import random
import pygame as pg
from .. import tools, prepare
from ..components import worlds, buildings, elves, decorations, transport_sleigh, landing_strip, clock_icon
from ..components.labels import Label

class Managing(tools._State):
    def __init__(self):
        super(Managing, self).__init__()
        self.next = None
        self.fps = 60
        self.min_speed = 20 #updates per second
        self.max_speed = 80
        self.speed = self.min_speed
        self.elapsed = 0.0
        self.world = worlds.World(3200, 2016, 16, 16)
        self.cursor = prepare.GFX["canecursor"]
        font = prepare.FONTS["weblysleekuili"]
        dark_font = prepare.FONTS["weblysleekuisl"]
        screen = pg.display.get_surface().get_rect()
        self.instruct_label = Label(font, 14, "Left-click to select an elf or building", "gray1",
                                               {"midtop": (screen.centerx, screen.top + 5)})
        self.instruct_label2 = Label(font, 14, "Right-click to open construction menu", "gray1",
                                                 {"midtop": (screen.centerx, self.instruct_label.rect.bottom + 2)})
        self.clock_icon = clock_icon.ClockIcon((screen.right - 50, screen.top + 20))
        self.clock_icon.update()
        self.help_icon = prepare.GFX["questionmark"]
        self.help_rect = self.help_icon.get_rect(topleft=(10, 10))
        self.paused = False
        self.pause_label = Label(dark_font, 96, "PAUSED", "darkgreen", {"center": screen.center})
        
        
        
        
        # TEST VALUES
        
        elf1 = elves.Elf((37, 20), self.world)
        elf2 = elves.Elf((38, 20), self.world)
        elf3 = elves.Elf((45, 30), self.world)
        elf4 = elves.Elf((3, 30), self.world)
        elf5 = elves.Elf((5, 30), self.world)
        elf10 = elves.Elf((57, 20), self.world)
        elf20 = elves.Elf((58, 20), self.world)
        elf30 = elves.Elf((55, 30), self.world)
        elf40 = elves.Elf((53, 30), self.world)
        elf50 = elves.Elf((45, 30), self.world)
        elf11 = elves.Elf((37, 20), self.world)
        elf22 = elves.Elf((38, 20), self.world)
        elf33 = elves.Elf((45, 30), self.world)
        elf44 = elves.Elf((6, 30), self.world)
        elf55 = elves.Elf((5, 30), self.world)
        elf1a = elves.Elf((37, 20), self.world)
        elf2a = elves.Elf((38, 20), self.world)
        elf3a = elves.Elf((45, 30), self.world)
        elf4a = elves.Elf((3, 30), self.world)
        elf5a = elves.Elf((5, 30), self.world)
        elf10a = elves.Elf((57, 20), self.world)
        elf20a = elves.Elf((58, 20), self.world)
        elf30a = elves.Elf((55, 30), self.world)
        elf40a = elves.Elf((53, 30), self.world)
        elf50a = elves.Elf((45, 30), self.world)
        elf11a = elves.Elf((37, 20), self.world)
        elf22a = elves.Elf((38, 20), self.world)
        elf33a = elves.Elf((45, 30), self.world)
        elf44a = elves.Elf((6, 30), self.world)
        elf55a = elves.Elf((5, 30), self.world)
        
        aelf1 = elves.Elf((37, 32), self.world)
        aelf2 = elves.Elf((38, 32), self.world)
        aelf3 = elves.Elf((45, 31), self.world)
        aelf4 = elves.Elf((3, 31), self.world)
        aelf5 = elves.Elf((5, 31), self.world)
        aelf10 = elves.Elf((57, 33), self.world)
        aelf20 = elves.Elf((58, 33), self.world)
        aelf30 = elves.Elf((55, 37), self.world)
        aelf40 = elves.Elf((53, 34), self.world)
        aelf50 = elves.Elf((45, 34), self.world)
        aelf11 = elves.Elf((37, 34), self.world)
        aelf22 = elves.Elf((38, 34), self.world)
        aelf33 = elves.Elf((45, 31), self.world)
        aelf44 = elves.Elf((6, 31), self.world)
        aelf55 = elves.Elf((5, 31), self.world)
        aelf1a = elves.Elf((37, 39), self.world)
        aelf2a = elves.Elf((38, 33), self.world)
        aelf3a = elves.Elf((45, 31), self.world)
        aelf4a = elves.Elf((3, 31), self.world)
        aelf5a = elves.Elf((5, 31), self.world)
        aelf10a = elves.Elf((57, 21), self.world)
        aelf20a = elves.Elf((58, 21), self.world)
        aelf30a = elves.Elf((55, 31), self.world)
        aelf40a = elves.Elf((53, 31), self.world)
        aelf50a = elves.Elf((45, 31), self.world)
        aelf11a = elves.Elf((37, 33), self.world)
        aelf22a = elves.Elf((38, 33), self.world)
        aelf33a = elves.Elf((45, 31), self.world)
        aelf44a = elves.Elf((6, 31), self.world)
        aelf55a = elves.Elf((5, 31), self.world)
        
        
        
        belf1 = elves.Elf((37, 32), self.world)
        belf2 = elves.Elf((38, 32), self.world)
        belf3 = elves.Elf((45, 31), self.world)
        belf4 = elves.Elf((3, 31), self.world)
        belf5 = elves.Elf((5, 31), self.world)
        belf10 = elves.Elf((57, 33), self.world)
        belf20 = elves.Elf((58, 33), self.world)
        belf30 = elves.Elf((55, 37), self.world)
        belf40 = elves.Elf((53, 34), self.world)
        belf50 = elves.Elf((45, 34), self.world)
        belf11 = elves.Elf((37, 34), self.world)
        belf22 = elves.Elf((38, 34), self.world)
        belf33 = elves.Elf((45, 31), self.world)
        belf44 = elves.Elf((6, 31), self.world)
        belf55 = elves.Elf((5, 31), self.world)
        belf1a = elves.Elf((37, 39), self.world)
        belf2a = elves.Elf((38, 33), self.world)
        belf3a = elves.Elf((45, 31), self.world)
        belf4a = elves.Elf((3, 31), self.world)
        belf5a = elves.Elf((5, 31), self.world)
        belf10a = elves.Elf((57, 21), self.world)
        belf20a = elves.Elf((58, 21), self.world)
        belf30a = elves.Elf((55, 31), self.world)
        belf40a = elves.Elf((53, 31), self.world)
        belf50a = elves.Elf((45, 31), self.world)
        belf11a = elves.Elf((37, 33), self.world)
        belf22a = elves.Elf((38, 33), self.world)
        belf33a = elves.Elf((45, 31), self.world)
        belf44a = elves.Elf((6, 31), self.world)
        belf55a = elves.Elf((5, 31), self.world)
        
        
        
        
        self.world.elves = [elf1, elf2, elf3, elf4, elf5, elf11, elf22, elf33,
                                    elf44, elf55, elf10, elf20, elf30, elf40, elf50, 
                                    elf1a, elf2a, elf3a, elf4a, elf5a, elf11a, elf22a,
                                    elf33a, elf44a, elf55a, elf10a, elf20a, elf30a,
                                    elf40a, elf50a, aelf1, aelf2, aelf3, aelf4, aelf5, 
                                    aelf11, aelf22, aelf33, aelf44, aelf55, aelf10,
                                    aelf20, aelf30, aelf40, aelf50, 
                                    aelf1a, aelf2a, aelf3a, aelf4a, aelf5a, aelf11a, aelf22a,
                                    aelf33a, aelf44a, aelf55a, aelf10a, aelf20a, aelf30a,
                                    aelf40a, aelf50a, belf1, belf2, belf3, belf4, belf5, 
                                    belf11, belf22, belf33, belf44, belf55, belf10,
                                    belf20, belf30, belf40, belf50, 
                                    belf1a, belf2a, belf3a, belf4a, belf5a, belf11a, belf22a,
                                    belf33a, belf44a, belf55a, belf10a, belf20a, belf30a,
                                    belf40a, belf50a]
        
        # END OF TEST VALUES
       
    def get_event(self, event):
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()
            elif event.key == pg.K_p:
                self.next = "PRESENTDROP"
                self.done = True
                
        elif event.type == pg.MOUSEBUTTONDOWN:
            #Testing - buildings should supersede elves
            if event.button == 1:
                if self.clock_icon.plus_rect.collidepoint(event.pos):
                    if self.paused:
                        self.paused = False
                    elif self.speed < self.max_speed:
                        self.speed += 20
                    return
                if self.clock_icon.minus_rect.collidepoint(event.pos):
                    if self.speed > self.min_speed:
                        self.speed -= 20
                    else:
                        self.paused = True
                    return
                if self.help_rect.collidepoint(event.pos):
                    self.next = "HELPMENU"
                    self.persist["helping"] = True
                    self.done = True
                    return
                
                deers = []
                for barn in [x for x in self.world.buildings if x.name == "Barn"]:
                    deers.extend(barn.reindeers)
                for deer in deers:
                    if deer.rect.collidepoint(event.pos):
                        self.persist["deer"] = deer
                        self.next = "DEERPOPUP"
                        self.done = True                        
                        return
                clicked_elves = []
                for elf in [x for x in self.world.elves if x.state in {"Hauling",
                                                                                         "Travelling", "Idle"}]:
                    if elf.rect.collidepoint(event.pos):
                        clicked_elves.append(elf)
                if len(clicked_elves) > 0:
                    if len(clicked_elves) == 1:                
                        self.persist["elf"] = clicked_elves[0]
                        self.persist["previous"] = "MANAGING"
                        self.persist["world"] = self.world
                        self.next = "ELFPOPUP"
                        self.done = True
                        return
                    else:
                        self.persist["elves"] = clicked_elves
                        self.next = "ELFSELECTOR"
                        self.persist["previous"] = "MANAGING"
                        self.done = True
                        return
                for ore in self.world.ores:
                    if ore.rect.collidepoint(event.pos):
                        self.persist["ore"] = ore
                        self.next = "MINEBUILD"
                        self.done = True
                        return
                for build in self.world.buildings:
                    if build.rect.collidepoint(event.pos):
                        self.persist["building"] = build
                        self.persist["previous"] = "MANAGING"
                        self.next = "BUILDINGPOPUP"
                        self.done = True
                        return
                for sign in self.world.travel_signs:
                    if sign.rect.collidepoint(event.pos):
                        if sign.destination == "Mt. Kringle":
                            self.next = "MOUNTAINGUIDE"
                            self.done = True
                        elif sign.destination == "Mistletoe Downs":
                            self.next = "BETINSTRUCTIONS"
                            self.done = True
                        elif sign.destination == "Spruce Glen DGC":
                            self.next = "GOLFING"
                            self.persist["player"] = self.player
                            self.done = True
                        return
                
            
            elif event.button == 3:
                self.next = "BUILDINGTYPESELECTION"
                self.persist["player"] = self.player
                self.persist["world"] = self.world
                self.done = True
                            
    def update(self, surface, keys, dt):
        mouse_pos = pg.mouse.get_pos()
        self.world.scroll(mouse_pos)
            
        if not pg.mixer.music.get_busy():
            pg.mixer.music.load(prepare.MUSIC["song1"])
            pg.mixer.music.play(-1)
        
        if not self.paused:
            self.elapsed += dt / 1000.0
            while self.elapsed >= 1.0 / self.speed:
                self.elapsed -= 1.0 / self.speed
                self.world.update()            
                self.clock_icon.update()
        
        self.draw(surface, mouse_pos)
        
    def draw(self, surface, mouse_pos):    
        self.world.draw(surface)
        self.instruct_label.draw(surface)
        self.instruct_label2.draw(surface)
        self.clock_icon.draw(surface)        
        surface.blit(self.help_icon, self.help_rect)
        if self.paused:
            self.pause_label.draw(surface)
        surface.blit(self.cursor, (mouse_pos))
        
    def startup(self, persistent):
        self.persist = persistent
        self.player = self.persist["player"]


    def cleanup(self):        
        self.persist["player"] = self.player
        self.persist["world"] = self.world
        self.done = False
        return self.persist
    
