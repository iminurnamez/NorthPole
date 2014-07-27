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
        self.max_fps = 80 #for testing, should be lower
        self.fps = 20
        self.world = worlds.World(3200, 2016, 16, 16)
        self.cursor = prepare.GFX["canecursor"]
        font = prepare.FONTS["weblysleekuili"]
        screen = pg.display.get_surface().get_rect()
        self.instruct_label = Label(font, 14, "Left-click to select an elf or building", "gray1",
                                               {"midtop": (screen.centerx, screen.top + 5)})
        self.instruct_label2 = Label(font, 14, "Right-click to open construction menu", "gray1",
                                                 {"midtop": (screen.centerx, self.instruct_label.rect.bottom + 2)})        
        self.clock_icon = clock_icon.ClockIcon((screen.right - 80, screen.top + 35))
        self.paused = False
        
        
        
        
        # TEST VALUES
        #barn1 = buildings.Barn((15, 15), self.world)
        #farm1 = buildings.MossFarm((30, 20), self.world)
        #farm2 = buildings.CarrotFarm((35, 20), self.world)
        #warehouse1 = buildings.Warehouse((30, 10), self.world)
        #elf_house = buildings.House((24, 22), self.world)
        #elf_house2 = buildings.House((24, 27), self.world)
        #ghouse = buildings.GingerbreadHouse((12, 34), self.world)
        #woodshed = buildings.WoodShed((5, 10), self.world)
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
        #elf1.assign_job(farm1)
        
        
        #elf2.assign_job(farm1)
        #elf3.assign_job(farm2)
        #elf4.assign_job(barn1)
        #elf5.assign_job(warehouse1)
        #elf10.assign_job(farm1)
        #elf20.assign_job(farm1)
        #elf30.assign_job(farm2)
        #elf40.assign_job(barn1)
        #elf50.assign_job(warehouse1)
        #elf11.assign_job(farm2)
        #elf22.assign_job(farm2)
        #elf33.assign_job(warehouse1)
        #elf44.assign_job(barn1)
        #elf55.assign_job(woodshed)
        #elf1a.assign_job(farm1)
        #elf2a.assign_job(farm1)
        #elf3a.assign_job(farm2)
        #elf4a.assign_job(barn1)
        #elf5a.assign_job(warehouse1)
        #elf10a.assign_job(farm1)
        #elf20a.assign_job(farm1)
        #elf30a.assign_job(farm2)
        #elf40a.assign_job(barn1)
        #elf50a.assign_job(warehouse1)
        #elf11a.assign_job(warehouse1)
        #elf22a.assign_job(warehouse1)
        #elf33a.assign_job(farm1)
        #elf44a.assign_job(barn1)
        #elf55a.assign_job(woodshed)
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
        #aelf1.assign_job(farm1)
        #aelf2.assign_job(farm1)
        #aelf3.assign_job(farm2)
        #aelf4.assign_job(barn1)
        #aelf5.assign_job(warehouse1)
        #aelf10.assign_job(warehouse1)
        #aelf20.assign_job(warehouse1)
        #aelf30.assign_job(farm2)
        #aelf40.assign_job(barn1)
        #aelf50.assign_job(warehouse1)
        #aelf11.assign_job(warehouse1)
        #aelf22.assign_job(warehouse1)
        #aelf33.assign_job(warehouse1)
        #aelf44.assign_job(barn1)
        #aelf55.assign_job(woodshed)
        #aelf1a.assign_job(warehouse1)
        #aelf2a.assign_job(warehouse1)
        #aelf3a.assign_job(warehouse1)
        #aelf4a.assign_job(barn1)
        #aelf5a.assign_job(warehouse1)
        #aelf10a.assign_job(warehouse1)
        #aelf20a.assign_job(warehouse1)
        #aelf30a.assign_job(warehouse1)
        #aelf40a.assign_job(barn1)
        #aelf50a.assign_job(warehouse1)
        #aelf11a.assign_job(warehouse1)
        #aelf22a.assign_job(warehouse1)
        #aelf33a.assign_job(warehouse1)
        #aelf44a.assign_job(barn1)
        #aelf55a.assign_job(woodshed)
        
        
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
        #belf1.assign_job(farm1)
        #belf2.assign_job(farm1)
        #belf3.assign_job(farm2)
        #belf4.assign_job(barn1)
        #belf5.assign_job(warehouse1)
        #belf10.assign_job(warehouse1)
        #belf20.assign_job(warehouse1)
        #belf30.assign_job(farm2)
        #belf40.assign_job(barn1)
        #belf50.assign_job(warehouse1)
        #belf11.assign_job(warehouse1)
        #belf22.assign_job(warehouse1)
        #belf33.assign_job(warehouse1)
        #belf44.assign_job(barn1)
        #belf55.assign_job(woodshed)
        #belf1a.assign_job(warehouse1)
        #belf2a.assign_job(warehouse1)
        #belf3a.assign_job(warehouse1)
        #belf4a.assign_job(barn1)
        #belf5a.assign_job(warehouse1)
        #belf10a.assign_job(warehouse1)
        #belf20a.assign_job(warehouse1)
        #belf30a.assign_job(warehouse1)
        #belf40a.assign_job(barn1)
        #belf50a.assign_job(warehouse1)
        #belf11a.assign_job(warehouse1)
        #belf22a.assign_job(warehouse1)
        #belf33a.assign_job(warehouse1)
        #belf44a.assign_job(barn1)
        #belf55a.assign_job(woodshed)
        
        
        
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
        #fort = buildings.SnowForts((41, 18), self.world)
        #theater = buildings.Theater((42, 10), self.world)
        #ctree = decorations.XmasTree((27, 18), self.world)
        #pyrobox = decorations.PyroBox((10, 20), self.world)
        #wavysanta = decorations.WavySanta((54, 30), self.world)
        #rink = buildings.SkatingRink((38, 35), self.world)
        #snackbar = buildings.SnackBar((34, 40), self.world)
        #carrotstand = buildings.CarrotStand((50, 10), self.world)
        #trees = [buildings.Tree((10, 10), self.world),
        #             buildings.Tree((12, 12), self.world),
        #             buildings.Tree((14, 42), self.world),
        #             buildings.Tree((45, 5), self.world),
        #             buildings.Tree((44, 30), self.world),
        #             buildings.Tree((20, 4), self.world),
        #             buildings.Tree((25, 6), self.world),
        #             buildings.Tree((30, 3), self.world)]
        #self.world.buildings = [farm1, farm2, elf_house, elf_house2, fort,
        #                                  barn1, warehouse1, theater, rink,
        #                                  woodshed, snackbar, ghouse, carrotstand]
        #self.world.food_buildings.append(snackbar)
        #self.world.cheer_buildings.append(fort)
        #self.world.cheer_buildings.append(theater)
        #self.world.rest_buildings.append(elf_house)
        #self.world.rest_buildings.append(elf_house2)
        #self.world.rest_buildings.append(ghouse)
        #self.world.cheer_buildings.append(rink)
        
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
                    elif self.fps < self.max_fps:
                        self.fps += 20
                    return
                if self.clock_icon.minus_rect.collidepoint(event.pos):
                    if self.fps > 20:
                        self.fps -= 20
                    else:
                        self.paused = True
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
                            
    def update(self, surface, keys):
        mouse_pos = pg.mouse.get_pos()
        self.world.scroll(mouse_pos)
            
        if not pg.mixer.music.get_busy():
            pg.mixer.music.load(prepare.MUSIC["song1"])
            pg.mixer.music.play(-1)
        
        if not self.paused:
            self.world.update()            
            self.clock_icon.update()
        
        self.draw(surface, mouse_pos)
        
    def draw(self, surface, mouse_pos):    
        self.world.draw(surface)
        self.instruct_label.draw(surface)
        self.instruct_label2.draw(surface)
        self.clock_icon.draw(surface)        
        surface.blit(self.cursor, (mouse_pos))
        
    def startup(self, persistent):
        pg.mouse.set_visible(False)
        self.persist = persistent
        self.player = self.persist["player"]


    def cleanup(self):
        pg.mouse.set_visible(True)
        
        self.persist["player"] = self.player
        self.persist["world"] = self.world
        self.done = False
        return self.persist
    
