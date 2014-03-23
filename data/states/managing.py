import sys
import random
import pygame as pg
from .. import tools, prepare
from ..components import worlds, buildings, elves, decorations


class Managing(tools._State):
    def __init__(self):
        super(Managing, self).__init__()
        self.next = None
        self.max_fps = 80 #for testing, should be lower
        self.fps = 20
        self.world = worlds.World(1600, 1008, 16, 16)

        # TEST VALUES
        barn1 = buildings.Barn((15, 15), self.world)
        farm1 = buildings.MossFarm((30, 20), self.world)
        farm2 = buildings.CarrotFarm((35, 20), self.world)
        warehouse1 = buildings.Warehouse((30, 10), self.world)
        elf_house = buildings.House((24, 22), self.world)
        elf_house2 = buildings.House((24, 27), self.world)
        ghouse = buildings.GingerbreadHouse((12, 34), self.world)
        woodshed = buildings.WoodShed((5, 10), self.world)
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
        elf1.job = farm1
        elf2.job = farm1
        elf3.job = farm2
        elf4.job = barn1
        elf5.job = warehouse1
        elf10.job = farm1
        elf20.job = farm1
        elf30.job = farm2
        elf40.job = barn1
        elf50.job = warehouse1
        elf11.job = farm2
        elf22.job = farm2
        elf33.job = warehouse1
        elf44.job = barn1
        elf55.job = woodshed
        elf1a.job = farm1
        elf2a.job = farm1
        elf3a.job = farm2
        elf4a.job = barn1
        elf5a.job = warehouse1
        elf10a.job = farm1
        elf20a.job = farm1
        elf30a.job = farm2
        elf40a.job = barn1
        elf50a.job = warehouse1
        elf11a.job = warehouse1
        elf22a.job = warehouse1
        elf33a.job = farm1
        elf44a.job = barn1
        elf55a.job = woodshed
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
        aelf1.job = farm1
        aelf2.job = farm1
        aelf3.job = farm2
        aelf4.job = barn1
        aelf5.job = warehouse1
        aelf10.job = warehouse1
        aelf20.job = warehouse1
        aelf30.job = farm2
        aelf40.job = barn1
        aelf50.job = warehouse1
        aelf11.job = warehouse1
        aelf22.job = warehouse1
        aelf33.job = warehouse1
        aelf44.job = barn1
        aelf55.job = woodshed
        aelf1a.job = warehouse1
        aelf2a.job = warehouse1
        aelf3a.job = warehouse1
        aelf4a.job = barn1
        aelf5a.job = warehouse1
        aelf10a.job = warehouse1
        aelf20a.job = warehouse1
        aelf30a.job = warehouse1
        aelf40a.job = barn1
        aelf50a.job = warehouse1
        aelf11a.job = warehouse1
        aelf22a.job = warehouse1
        aelf33a.job = warehouse1
        aelf44a.job = barn1
        aelf55a.job = woodshed
        self.world.elves = [elf1, elf2, elf3, elf4, elf5, elf11, elf22, elf33,
                                    elf44, elf55, elf10, elf20, elf30, elf40, elf50, 
                                    elf1a, elf2a, elf3a, elf4a, elf5a, elf11a, elf22a,
                                    elf33a, elf44a, elf55a, elf10a, elf20a, elf30a,
                                    elf40a, elf50a, aelf1, aelf2, aelf3, aelf4, aelf5, 
                                    aelf11, aelf22, aelf33, aelf44, aelf55, aelf10,
                                    aelf20, aelf30, aelf40, aelf50, 
                                    aelf1a, aelf2a, aelf3a, aelf4a, aelf5a, aelf11a, aelf22a,
                                    aelf33a, aelf44a, aelf55a, aelf10a, aelf20a, aelf30a,
                                    aelf40a, aelf50a]
        fort = buildings.SnowForts((41, 18), self.world)
        theater = buildings.Theater((42, 10), self.world)
        ctree = decorations.XmasTree((27, 18), self.world)
        pyrobox = decorations.PyroBox((10, 20), self.world)
        wavysanta = decorations.WavySanta((54, 30), self.world)
        rink = buildings.SkatingRink((38, 35), self.world)
        snackbar = buildings.SnackBar((34, 40), self.world)
        carrotstand = buildings.CarrotStand((50, 10), self.world)
        self.world.trees = [buildings.Tree((10, 10), self.world),
                                    buildings.Tree((12, 12), self.world),
                                    buildings.Tree((14, 42), self.world),
                                    buildings.Tree((45, 5), self.world),
                                    buildings.Tree((44, 30), self.world),
                                    buildings.Tree((20, 4), self.world),
                                    buildings.Tree((25, 6), self.world),
                                    buildings.Tree((30, 3), self.world)]
        self.world.buildings = [farm1, farm2, elf_house, elf_house2, fort,
                                          barn1, warehouse1, theater, rink,
                                          woodshed, snackbar, ghouse, carrotstand]
        self.world.food_buildings.append(snackbar)
        self.world.cheer_buildings.append(fort)
        self.world.cheer_buildings.append(theater)
        self.world.rest_buildings.append(elf_house)
        self.world.rest_buildings.append(elf_house2)
        self.world.rest_buildings.append(ghouse)
        self.world.decorations.append(ctree)
        self.world.decorations.append(pyrobox)
        self.world.decorations.append(wavysanta)
        self.world.cheer_buildings.append(rink)
        # END OF TEST VALUES
       
    def get_event(self, event):
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()
            elif event.key == pg.K_s:
                self.next = "MOUNTAINGUIDE"
                pg.mixer.music.stop()
                self.done = True
            elif event.key == pg.K_r:
                self.next = "BETINSTRUCTIONS"
                pg.mixer.music.stop()
                self.done = True
            elif event.key == pg.K_DOWN:
                if self.fps > 20:
                    self.fps -= 10
            elif event.key == pg.K_UP:
                if self.fps < self.max_fps:
                    self.fps += 10
        elif event.type == pg.MOUSEBUTTONDOWN:
            #Testing - buildings should supercede elves
            for elf in [x for x in self.world.elves if x.state in {"Hauling",
                                                                                     "Travelling", "Idle"}]:
                if elf.rect.collidepoint(event.pos):
                    self.persist["elf"] = elf
                    self.persist["previous"] = "MANAGING"
                    self.next = "ELFPOPUP"
                    self.done = True
                    break
            for build in self.world.buildings:
                if build.rect.collidepoint(event.pos):
                    self.persist["building"] = build
                    self.persist["previous"] = "MANAGING"
                    self.next = "BUILDINGPOPUP"
                    self.done = True
                    break

    def update(self, surface, keys):
        self.world.update()            
        surface.fill(pg.Color("grey96"))
        self.world.display(surface)

    def startup(self, persistant):
        self.player = persistant["player"]
        if not pg.mixer.music.get_busy():
            pg.mixer.music.load(prepare.MUSIC["song1"])
            pg.mixer.music.play(-1)
        return tools._State.startup(self, persistant)    

    def cleanup(self):
        self.persist["player"] = self.player
        self.done = False
        return self.persist
    
