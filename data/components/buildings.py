import itertools as it
from collections import defaultdict
import random
import pygame as pg
from .. import prepare
from elves import Reindeer

class Window(object):
    def __init__(self, lefttop, size):
        self.rect = pg.Rect(lefttop, size)
        self.color_range = range(130, 155, 1)
        self.colors = self.color_range
        self.color = random.choice(self.colors)
        
    def update(self, world):
        if world.ticks % 5 == 0:
            self.color = random.choice(self.colors)
            
    def display(self, surface, on):
        if on:
            pg.draw.rect(surface, (255, self.color, 0), self.rect)
        else:
            pg.draw.rect(surface, pg.Color("gray10"), self.rect)
            
            
class HouseTreeLights(object):
    def __init__(self, lefttop):
        self.images = it.cycle([prepare.GFX["housetreelights1"], prepare.GFX["housetreelights2"], 
                                         prepare.GFX["housetreelights3"], prepare.GFX["housetreelights4"]])
        self.image = next(self.images)
        self.rect = self.image.get_rect(topleft=lefttop)
        
    def update(self, world):
        if world.ticks % 5 == 0:
            self.image = next(self.images)
                       
    def display(self, surface, on):
        if on:
            surface.blit(self.image, self.rect)

            
class Tile(object):
    def __init__(self, index, name, world): 
        self.name = name
        self.index = index
        self.rect = pg.Rect(world.grid[self.index].rect.topleft, (16, 16))
        self.image = next(self.images)
                
    def display(self, surface):
        surface.blit(self.image, self.rect)
        
class MossTile(Tile):
    def __init__(self, index, world):
        self.images = it.cycle([prepare.GFX["moss1"], prepare.GFX["moss2"],
                                         prepare.GFX["moss3"], prepare.GFX["moss4"], 
                                         prepare.GFX["moss5"]])
        super(MossTile, self).__init__(index, "Moss", world)
        
class CarrotTile(Tile):
    def __init__(self, index, world):
        self.images = it.cycle([prepare.GFX["carrot1"], prepare.GFX["carrot2"],
                                         prepare.GFX["carrot3"], prepare.GFX["carrot4"], 
                                         prepare.GFX["carrot5"]])
        super(CarrotTile, self).__init__(index, "Carrot", world)

class SnowTile(Tile): 
    def __init__(self, index, world):
        self.images = it.cycle([prepare.GFX["snow"]])
        super(SnowTile, self).__init__(index, "Snow", world)
        
        
class BuildingTile(object):
    def __init__(self, index, name, image_name, world):
        self.index = index
        self.name = name
        self.image = prepare.GFX[image_name]
        lefttop = world.grid[self.index].rect.topleft
        self.rect = self.image.get_rect(bottomleft=(lefttop[0], lefttop[1] + 16))
        

    def display(self, surface):
        surface.blit(self.image, self.rect)

class WarehouseTile(BuildingTile):
    def __init__(self, index, world):
        super(WarehouseTile, self).__init__(index, "Warehouse", "warehouse", world)
        
class BarnTile(BuildingTile):
    def __init__(self, index, world):
        super(BarnTile, self).__init__(index, "Barn", "barn", world)
        
class PottingShed(BuildingTile):
    def __init__(self, index, world):
        super(PottingShed, self).__init__(index, "Potting Shed", "pottingshed", world)
        
class WoodShedTile(BuildingTile):
    def __init__(self, index, world):
        super(WoodShedTile, self).__init__(index, "Wood Shed", "woodshed", world)
        
class HouseTile(BuildingTile):
    def __init__(self, index, world):
        super(HouseTile, self).__init__(index, "House", "elfhouse", world)

class GingerHouseTile(BuildingTile):
    def __init__(self, index, world):
        super(GingerHouseTile, self).__init__(index, "Gingerbread House", "gingerbreadhouse", world)        
        
class FortsTile(BuildingTile):
    def __init__(self, index, world):
        super(FortsTile, self).__init__(index, "Snow Forts", "forts", world)

class TreeTile(BuildingTile):
    def __init__(self, index, world):
        super(TreeTile, self).__init__(index, "Tree", "tree", world)
        
class TheaterTile(BuildingTile):
    def __init__(self, index, world):
        super(TheaterTile, self).__init__(index, "Theater", "theater", world)
        
class RinkTile(BuildingTile):
    def __init__(self, index, world):
        super(RinkTile, self).__init__(index, "Skating Rink", "rink", world)
        
class SnackBarTile(BuildingTile):
    def __init__(self, index, world):
        super(SnackBarTile, self).__init__(index, "Snack Bar", "snackbar", world)
        
class CarrotStandTile(BuildingTile):
    def __init__(self, index, world):
        super(CarrotStandTile, self).__init__(index, "Carrot Stand", "carrotstand", world)

class Building(object):
    def __init__(self, name, index, entrance, world, size, tile_map, char_map):
        self.name = name
        self.index = index
        self.entrance = (self.index[0] + entrance[0], self.index[1] + entrance[1])        
        self.rect = pg.Rect(world.grid[self.index].rect.topleft, size)
        self.tile_map = tile_map
        self.char_map = char_map
        self.windows = []
        self.workers = []
        self.max_workers = 0
        self.patrons = []
        self.max_patrons = 0
        self.en_route_workers = []
        self.en_route_patrons = []
        self.outputs = {}
        self.inputs = {}
        self.tiles = []
        column = len(self.tile_map[0]) - 1
        row = 0
        right = 16
        top = 0
        for line in self.tile_map:
            for char in line[::-1]:
                index = (self.index[0] + column,
                              self.index[1] + row)
                if char != "X":
                    world.grid[index].occupied = True
                try:
                    tile = self.char_map[char](index, world)
                    self.tiles.append(tile)
                except KeyError:
                    pass
                right += 16
                column -= 1
            row += 1
            column = len(self.tile_map[0]) - 1
            top += 16
            right = 16
        world.grid[self.entrance].occupied = False
        
    def has_patron_vacancies(self):
        return (len(self.en_route_patrons) + len(self.patrons) <
                                                                 self.max_patrons)
                                                                 
    def has_worker_vacancies(self):
        return (len(self.en_route_workers) + len(self.workers) <
                                                                 self.max_workers)
                                                                 
    def move(self, offset):
        self.rect.move(offset)
        for tile in it.chain(self.tiles, self.windows):
            tile.move_ip(offset)
    
    def update(self, world):
        for window in self.windows:
            window.update(world)
            
    def display(self, surface):
        for window in self.windows:
            window.display(surface, max([len(self.patrons), len(self.workers)]))
        for tile in self.tiles:
            tile.display(surface)
       
class Warehouse(Building):
    def __init__(self, index, world):
        tile_map =  ["XXXXXXX",
                          "OOOOOOO",
                          "OOOOOOO",
                          "OOOOOOO",
                          "OOOOOOO",
                          "OOOOOOO",
                          "WOOOOOO"]
        char_map = {"W": WarehouseTile}                  
        super(Warehouse, self).__init__("Warehouse", index, (2, 6), world,
                                                        (112, 112), tile_map, char_map)
        self.outputs = defaultdict(int)
        self.door_image = prepare.GFX["warehousedoor"]
        door_rect = self.door_image.get_rect(topleft=self.rect.topleft)
        self.door_rects = [door_rect.move(28, 96), door_rect.move(57, 96)]

        self.workers = []
        self.max_workers = 12

    def display(self, surface):
        for window in self.windows:
            window.display(surface, len(self.workers))
        for tile in self.tiles:
            tile.display(surface)
        if not self.workers:
            for door_rect in self.door_rects:
                surface.blit(self.door_image, door_rect)
                
class Tree(Building):
    def __init__(self, index, world):
        tile_map = ["XX",
                          "TX"]
        char_map = {"T": TreeTile}
        super(Tree, self).__init__("Tree", index, (1, 1), world, (32, 32),
                                              tile_map, char_map)
        self.wood = 1000
        self.outputs["wood"] = 0
        self.max_workers = 1
  
    def update(self, world):            
        if self.wood < 1:
            world.trees.remove(self)
        
    def display(self, surface):
        for tile in self.tiles:
            tile.display(surface)
        
    
class House(Building):
    def __init__(self, index, world):
        tile_map = ["XXXX",
                          "OOOO",
                          "OOOO",
                          "OOOO",
                          "HOXO"]
        char_map = {"H": HouseTile}
        super(House, self).__init__("House", index, (2, 4), world, (64, 80),
                                                 tile_map, char_map)
        self.windows = [Window((self.rect.left + 11, self.rect.top + 53),
                                             (17, 18))]
        self.lights = HouseTreeLights((self.rect.left + 15, self.rect.top + 60))
        self.max_patrons = 6
        
    def move(self, offset):
        for tile in it.chain(self.rect, self.tiles, self.windows, self.lights):
            tile.move_ip(offset)
        
    def update(self, world):
        for window in self.windows:
            window.update(world)
        self.lights.update(world)
    
    def display(self, surface):
        for window in self.windows:
            window.display(surface, len(self.patrons))
        for tile in self.tiles:
            tile.display(surface)
        self.lights.display(surface, len(self.patrons))

        
class GingerbreadHouse(Building):
    def __init__(self, index, world):
        tile_map = ["XXXXX",
                           "XXXXX",
                           "OOOOO",
                           "OOOOO",
                           "OOOOO",
                           "GOOOO"]
        char_map = {"G": GingerHouseTile}
        super(GingerbreadHouse, self).__init__("Gingerbread House", index, (2, 5), world,
                                                                   (80, 96), tile_map, char_map)
        coords = [(16, 41), (16, 61), (34, 41), (52, 41), (52, 61)]
        self.window_spots = [(self.rect.left + x[0], self.rect.top + x[1]) for x in coords]
        self.windows = [Window(y, (10, 10)) for y in self.window_spots]
        self.window_images = it.cycle([prepare.GFX["candywindow" + str(z)] for z in range(1, 10)])
        self.window_image = next(self.window_images)
        self.dimmer = pg.Surface((10, 10)).convert_alpha()
        pg.draw.rect(self.dimmer, (0, 0, 0, 60), self.dimmer.get_rect().inflate(-2, -2))
        self.max_patrons = 8
                                     
    def update(self, world):
        if self.patrons and not world.ticks % 6:
            self.window_image = next(self.window_images)
        for window in self.windows:
            window.update(world)
        
    def display(self, surface):
        for tile in self.tiles:
            tile.display(surface)
        for window in self.windows:
            window.display(surface, len(self.patrons))            
        for spot in self.window_spots:
            surface.blit(self.dimmer, spot)
            surface.blit(self.window_image, spot)

        
class Barn(Building):
    def __init__(self, index, world):
        tile_map = ["XXXXXXX",
                          "OOOOOOO",
                          "OOOOOOO",
                          "OOOOOOO",
                          "OOOOOOO",
                          "OOOOOOO",
                          "BOOOOOO"]
        char_map = {"B": BarnTile}        
        super(Barn, self).__init__("Barn", index, (4, 6), world, (112, 112),
                                               tile_map, char_map)
        self.door_image = prepare.GFX["barndoor"]
        self.open_rect = self.door_image.get_rect(topleft=(self.rect.left + 38, self.rect.top + 41))
        self.shut_rect = self.door_image.get_rect(topleft=(self.rect.left + 49, self.rect.top + 41))
        #self.open_door = prepare.GFX["barndooropen"]
        #self.shut_door = prepare.GFX["barndoorshut"]
        #self.door_rect = self.shut_door.get_rect(topleft=(self.rect.left + 39, self.rect.top + 40))
        self.deer_rect = pg.Rect(self.rect.left + 1, self.rect.top + 45 , 109, 65) 
        self.reindeers = [Reindeer(self.rect.center, random.randint(1, 10), self),
                                 Reindeer(self.rect.center, random.randint(1, 10), self)]
        self.outputs["Milk"] = 0
        self.inputs["Moss"] = 0
        self.inputs["Carrot"] = 0
        self.max_workers = 2
        
    def update(self, world):
        for deer in self.reindeers:
            deer.update(world)

    def move(self, offset):
        for tile in it.chain([self.rect, self.deer_rect], self.tiles, self.reindeers):
            tile.move_ip(offset)    
    
    def display(self, surface):
        for window in self.windows:
            window.display(surface, len(self.workers))
        for tile in self.tiles:
            tile.display(surface)
        if self.workers:
            #surface.blit(self.open_door, self.door_rect)
            surface.blit(self.door_image, self.open_rect)
        else:
            #surface.blit(self.shut_door, self.door_rect)
            surface.blit(self.door_image, self.shut_rect)
        for reindeer in self.reindeers:
            reindeer.display(surface)        

            
class MossFarm(Building):
    def __init__(self, index, world):
        tile_map = ["XXXX",
                          "OOMM",
                          "SOMM",
                          "MMMM",
                          "MMMM"]
        char_map = {"M": MossTile,
                             "S": PottingShed}
        super(MossFarm, self).__init__("Moss Farm", index, (0, 2), world,
                                                      (64, 80), tile_map, char_map)
        self.windows = [Window((self.rect.left + 9, self.rect.top + 18), (7, 7))]
        self.growth = 1
        self.outputs["Moss"] = 0
        self.max_workers = 2
        
    def update(self, world):
        for window in self.windows:
            window.update(world)
        for worker in self.workers:
            self.growth += 1  #TODO: should be from elf skill
        if self.growth % 300 == 0:
            for tile in self.tiles:
                try:
                    tile.image = next(tile.images)
                except AttributeError:
                    pass
        if self.growth > 1500:
            self.outputs["Moss"] += 100    # TODO: should be from elf skill if growth isn't
            self.growth = 1
            
            
class CarrotFarm(Building):
    def __init__(self, index, world):
        tile_map = ["XXXX",
                          "OOCC",
                          "SOCC",
                          "CCCC",
                          "CCCC"]
        char_map = {"C": CarrotTile,
                             "S": PottingShed}
        super(CarrotFarm, self).__init__("Carrot Farm", index, (0, 2), world,
                                                        (64, 80), tile_map, char_map)
        self.windows = [Window((self.rect.left + 9, self.rect.top + 18), (7, 7))]
        self.growth = 0
        self.current_growth = 0
        self.outputs["Carrot"] = 0
        self.max_workers = 2
        
    def update(self, world):
        for window in self.windows:
            window.update(world)
        for worker in self.workers:
            self.growth += 1  #TODO: should be from elf skill and use growth stages not modulo
            self.current_growth += 1
        if self.current_growth > 300:
            self.current_growth -= 300
            for tile in self.tiles:
                try:
                    tile.image = next(tile.images)
                except AttributeError:
                    pass                
        if self.growth > 1500:
            self.outputs["Carrot"] += 100
            self.growth = 0
            self.current_growth = 0


class WoodShed(Building):
    def __init__(self, index, world):
        tile_map = ["OX",
                          "WO"]
        char_map = {"W": WoodShedTile}
        super(WoodShed, self).__init__("Wood Shed", index, (0, 1), world,
                                                      (32, 32), tile_map, char_map)
        self.outputs["Wood"] = 0
        self.max_workers = 4
        
           
class Snowball(object):
    def __init__(self, group, lefttop, offsets):
        self.coords = iter([(lefttop[0] + x[0], lefttop[1] + x[1]) for x in offsets])
        self.coord = next(self.coords)
        self.image = prepare.GFX["snowball"]
        self.rect = self.image.get_rect(center=self.coord)
        self.group = group
        self.group.append(self)
        
    def update(self, world):
        if not world.ticks % 2:
            try:
                self.coord = next(self.coords)
                self.rect.center = self.coord
            except StopIteration:
                self.group.remove(self)
    
    def display(self, surface):
        surface.blit(self.image, self.rect)

        
class Thrower(object):
    def __init__(self, building, side, lefttop):
        self.building = building
        self.images = it.cycle([prepare.GFX[side + "thrower1"], 
                                          prepare.GFX[side + "thrower2"],
                                          prepare.GFX[side + "thrower3"], 
                                          prepare.GFX[side + "thrower4"]])
        self.image = next(self.images)
        self.rect = self.image.get_rect(topleft=lefttop)
        self.throwing = False
        self.counter = 1
 
    def move(self, offset):
        self.rect.move_ip(offset)

    def update(self, world):
        if not self.throwing and random.randint(1, 100) < 10:
            self.throwing = True        
        elif self.throwing and world.ticks % 3 == 0:
            self.image = next(self.images)
            self.counter += 1
        if self.counter == 4:
            snowball = Snowball(self.building.snowballs, self.building.rect.topleft, self.offsets)
            self.counter = 1
            self.throwing = False
            
    def display(self, surface):
        surface.blit(self.image, self.rect)
        
class LeftThrower(Thrower):
    def __init__(self, building, lefttop):
        super(LeftThrower, self).__init__(building, "left", lefttop)    
        self.offsets = [(47,24),(49,22),(53,19),(57,16),(61,14),(65,12),
                             (69,10), (73,9),(77,9),(81,10),(85,12),(89, 14),
                             (93, 16),(97, 19), (101, 122),(104, 25),(107, 28)]
        
class RightThrower(Thrower):
    def __init__(self, building, lefttop):
        super(RightThrower, self).__init__(building, "right", lefttop)    
        self.offsets = [(110, 21),(106, 18),(102, 15),(92,13),(94,11),(90,9),
                             (86,8),(82,8),(78,9),(74,11),(70,13),(66,15),(62,18),
                             (58,21),(55,24),(52,27)]
                 
class SnowForts(Building):
    def __init__(self, index, world):
        tile_map = ["OOOOOOOOOO",
                          "XOOOOOOOOO", 
                          "FOOOOOOOOO"]
        char_map = {"F": FortsTile}
        super(SnowForts, self).__init__("Snow Forts", index, (0, 1), world,
                                                       (160, 48), tile_map, char_map)
        self.throwers = [LeftThrower(self, (self.rect.left + 37,
                                                           self.rect.top + 24)), 
                                RightThrower(self, (self.rect.left + 115,
                                                             self.rect.top + 24))]
        self.snowballs = []
        self.max_patrons = 8
        
    def update(self, world):
        if self.patrons:
            for elem in it.chain(self.throwers, self.snowballs):
                elem.update(world)
            
    def move(self, offset):
        self.rect.move_ip(offset)
        for elem in it.chain(self.throwers, self.snowballs):
            elem.rect.move_ip(offset)

    def give_cheer(self, elf):
        if len(self.patrons) > 1:
            elf.cheer += 1.5
            elf.energy -= .5
    
    def display(self, surface):
        for tile in self.tiles:
            tile.display(surface)
        if len(self.patrons) > 1:
            for elem in it.chain(self.throwers, self.snowballs):
                elem.display(surface)
                
                
class Theater(Building):
    def __init__(self, index, world):
        tile_map = ["XXX",
                          "OOO",
                          "OOO", 
                          "TOO"]
        char_map = {"T": TheaterTile}
        super(Theater, self).__init__("Theater", index, (0, 3), world,
                                                       (48, 64), tile_map, char_map)
        self.puppet_images = it.cycle([prepare.GFX["puppet" + str(x)] for x in range(1, 18)])
        self.puppet_image = next(self.puppet_images)
        self.curtain_image = prepare.GFX["curtain"]
        self.patron_image = prepare.GFX["showpatron"]
        self.stage_rect = (self.rect.left + 17, self.rect.top + 25, 14, 9)
        patron_offsets = [(22, 40), (14, 50), (31, 40), (29, 50), (13, 40), (21, 50)]
        self.patron_rects = [pg.Rect(self.rect.left + x[0], self.rect.top + x[1], 5, 14) for x in patron_offsets]
        self.in_use = 0
        self.max_patrons = 6
        
    def update(self, world):
        if self.patrons:
            if not world.ticks % 7:
                self.puppet_image = next(self.puppet_images)
        
    def move(self, offset):
        self.rect.move_ip(offset)
        for elem in it.chain(self.throwers, self.snowballs):
            elem.rect.move_ip(offset)

    def give_cheer(self, elf):
        elf.cheer += 1
        elf.energy += .3
    
    
    def display(self, surface):
        for tile in self.tiles:
            tile.display(surface)
        if self.patrons:      
            surface.blit(self.puppet_image, self.stage_rect)
            for prect in self.patron_rects[:len(self.patrons)]:
                surface.blit(self.patron_image, prect)
        else:
            surface.blit(self.curtain_image, self.stage_rect)

            
class Skater(object):
    def __init__(self, lefttop):
        self.images = {-1: it.cycle([prepare.GFX["skaterleft1"], 
                                                prepare.GFX["skaterleft2"],
                                                prepare.GFX["skaterleft3"],
                                                prepare.GFX["skaterleft2"],
                                                prepare.GFX["skaterleft3"]]),
                               1: it.cycle([pg.transform.flip(prepare.GFX["skaterleft1"],
                                                                          True, False), 
                                                pg.transform.flip(prepare.GFX["skaterleft2"],
                                                                          True, False),
                                                pg.transform.flip(prepare.GFX["skaterleft3"],
                                                                          True, False),
                                                pg.transform.flip(prepare.GFX["skaterleft2"],
                                                                          True, False),
                                                pg.transform.flip(prepare.GFX["skaterleft3"],
                                                                          True, False)])} 
        self.x_velocity = random.choice((-1, 1))
        self.y_velocity = random.randint(-1, 1)
        self.image = next(self.images[self.x_velocity])
        self.rect = self.image.get_rect(topleft=lefttop)
        
    def update(self, world, rink_rect):
        if not world.ticks % 9:
            self.image = next(self.images[self.x_velocity])
        if not random.randint(0, 200):
            self.y_velocity = random.randint(-1, 1)
        self.rect.move_ip((self.x_velocity, self.y_velocity))
        if self.rect.top < rink_rect.top or self.rect.bottom > rink_rect.bottom:        
            self.y_velocity *= -1
        if self.rect.left < rink_rect.left or self.rect.right > rink_rect.right:
            self.x_velocity *= -1
        
    def display(self, surface):
        surface.blit(self.image, self.rect)

        
class SkatingRink(Building):
    def __init__(self, index, world):
        tile_map = ["OOOOOOOOOOOO",
                          "OOOOOOOOOOOO",
                          "OOOOOOOOOOOO",
                          "OOOOOOOOOOOO", 
                          "ROOOOOOOOOOO"]
        char_map = {"R": RinkTile}
        super(SkatingRink, self).__init__("Skating Rink", index, (9, 0),
                                                          world, (192, 80), tile_map,
                                                          char_map)
        self.rink_rect = pg.Rect(self.rect.left + 18, self.rect.top, 152, 68) 
        self.skaters = []
        self.max_patrons = 10
        
    def update(self, world):
        if len(self.skaters) < len(self.patrons):
            x = random.randint(self.rink_rect.left + 5,
                                          self.rink_rect.right - 21)
            y = random.randint(self.rink_rect.top,
                                          self.rink_rect.bottom - 21)
            self.skaters.append(Skater((x, y)))
        if len(self.skaters) > len(self.patrons):
            self.skaters = self.skaters[1:]
        for skater in self.skaters:
            skater.update(world, self.rink_rect)
        
    def move(self, offset):
        self.rect.move_ip(offset)
        for skater in self.skaters:
            skater.rect.move_ip(offset)

    def give_cheer(self, elf):
        elf.cheer += 2.5
        elf.energy += 1
        
    def display(self, surface):
        for tile in self.tiles:
            tile.display(surface)
        for skater in self.skaters:
            skater.display(surface)

class SnackBar(Building):
    def __init__(self, index, world):
        tile_map = ["OOOO",
                          "OOOO",
                          "OOOO", 
                          "BOOO"]
        char_map = {"B": SnackBarTile}
        super(SnackBar, self).__init__("Snack Bar", index, (0, 2), world,
                                                      (64, 64), tile_map, char_map)
        self.up_slots = [(4, 41), (13, 41), (21, 41), (38, 41), (48, 41),
                                (56, 41)]
        self.down_slots = [(4, 50), (13, 50), (22, 50), (39, 50), (47, 50),
                                    (55, 50)]
        self.slots = self.up_slots + self.down_slots
        self.patron_images = {41: prepare.GFX["downpatron"],
                                          50: prepare.GFX["uppatron"]}
        self.patron_rects = []
        self.max_patrons = 12
        self.inputs["Milk"] = 1000  #Testing - should be 0
        self.inputs["Cookies"] = 0
    
    def update(self, world):
        for key in self.inputs:
            if self.inputs[key] < 0:
                self.inputs[key] = 0
        if len(self.patron_rects) < len(self.patrons):
            self.patron_rects.append(random.choice(
                                          [x for x in self.slots if x not in self.patron_rects]))
        elif len(self.patron_rects) > len(self.patrons):
            diff = len(self.patron_rects) - len(self.patrons)
            self.patron_rects = self.patron_rects[diff:]
        
            
    def display(self, surface):
        for tile in self.tiles:
            tile.display(surface)
        for patron_rect in self.patron_rects:
            surface.blit(self.patron_images[patron_rect[1]], 
                             (self.rect.left + patron_rect[0],
                             self.rect.top + patron_rect[1]))
                             
                    
class CarrotStand(Building):
    def __init__(self, index, world):
        tile_map = ["OO",
                          "OO", 
                          "BO"]
        char_map = {"B": CarrotStandTile}
        super(CarrotStand, self).__init__("Carrot Stand", index, (1, 2),
                                                          world, (32, 48), tile_map,
                                                          char_map)
        self.food_rect = pg.Rect(self.rect.left - 32, self.rect.top, 96, 96)
        self.inputs["Carrot"] = 10
        
    def move(self, offset):
        self.rect.move_ip(offset)
        self.food_rect.move_ip(offset)
        
    def update(self, world):
        elves = world.elves
        for elf in [x for x in elves if x.rect.colliderect(self.food_rect)]:
            if self.inputs["Carrot"] >= .2:
                elf.food += .2
                self.inputs["Carrot"] -= .2
                if elf.food > elf.max_food:
                    elf.food = elf.max_food
    
     