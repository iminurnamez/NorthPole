import itertools as it
from collections import defaultdict
import random
import pygame as pg
from .. import prepare
from elves import Reindeer

class Window(object):
    def __init__(self, lefttop, size):
        self.rect = pg.Rect(lefttop, size)
        self.color_range = range(140, 155, 1)
        self.colors = self.color_range
        self.color = random.choice(self.colors)
        
    def update(self, world):
        if world.ticks % 5 == 0:
            self.color = random.choice(self.colors)
            
    def draw(self, surface, on):
        if on:
            pg.draw.rect(surface, (255, self.color, 0), self.rect)
        else:
            pg.draw.rect(surface, pg.Color("gray20"), self.rect)
            
            
class HouseTreeLights(object):
    def __init__(self, lefttop):
        self.images = it.cycle([prepare.GFX["housetreelights1"], prepare.GFX["housetreelights2"], 
                                         prepare.GFX["housetreelights3"], prepare.GFX["housetreelights4"]])
        self.image = next(self.images)
        self.rect = self.image.get_rect(topleft=lefttop)
        
    def update(self, world):
        if world.ticks % 5 == 0:
            self.image = next(self.images)
                       
    def draw(self, surface, on):
        if on:
            surface.blit(self.image, self.rect)

            
class Tile(object):
    def __init__(self, index, name, world): 
        self.name = name
        self.index = index
        self.rect = pg.Rect(world.grid[self.index].rect.topleft, (16, 16))
        self.image = next(self.images)
                
    def draw(self, surface):
        surface.blit(self.image, self.rect)

        
class MossTile(Tile):
    def __init__(self, index, world):
        names  = ["moss" + str(x) for x in range(1, 6)]
        self.images = it.cycle([prepare.GFX[name] for name in names])
        super(MossTile, self).__init__(index, "Moss", world)
        
class BeetTile(Tile):
    def __init__(self, index, world):
        names = ["beet" + str(x) for x in range(1, 6)]
        self.images = it.cycle([prepare.GFX[name] for name in names])
        super(BeetTile, self).__init__(index, "Beet", world)
        
class CarrotTile(Tile):
    def __init__(self, index, world):
        names  = ["carrot" + str(x) for x in range(1, 6)]
        self.images = it.cycle([prepare.GFX[name] for name in names])
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
        
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
    def move(self, offset):
        self.rect.move_ip(offset)

class WarehouseTile(BuildingTile):
    def __init__(self, index, world):
        super(WarehouseTile, self).__init__(index, "Warehouse", "warehouse", world)
        
class BarnTile(BuildingTile):
    def __init__(self, index, world):
        super(BarnTile, self).__init__(index, "Barn", "barn", world)
        
class BakeryTile(BuildingTile):
    def __init__(self, index, world):
        super(BakeryTile, self).__init__(index, "Bakery", "bakery", world)

class DentistOfficeTile(BuildingTile):
    def __init__(self, index, world):
        super(DentistOfficeTile, self).__init__(index, "Dentist's Office", "dentistoffice", world)

class SchoolTile(BuildingTile):
    def __init__(self, index, world):
        super(SchoolTile, self).__init__(index, "Schoolhouse", "school", world)
        
class PottingShed(BuildingTile):
    def __init__(self, index, world):
        super(PottingShed, self).__init__(index, "Potting Shed", "pottingshed", world)
        
class WoodShedTile(BuildingTile):
    def __init__(self, index, world):
        super(WoodShedTile, self).__init__(index, "Wood Shed", "woodshed", world)
        
class MineTile(BuildingTile):
    def __init__(self, index, world):
        super(MineTile, self).__init__(index, "Mine", "mine", world)
        
class HouseTile(BuildingTile):
    def __init__(self, index, world):
        super(HouseTile, self).__init__(index, "House", "elfhouse", world)

class IglooTile(BuildingTile):
    def __init__(self, index, world):
        super(IglooTile, self).__init__(index, "Igloo", "igloo", world)
        
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

class OreTile(BuildingTile):
    def __init__(self, index, world):
        super(OreTile, self).__init__(index, "Ore", "ore", world)
        
class SnackBarTile(BuildingTile):
    def __init__(self, index, world):
        super(SnackBarTile, self).__init__(index, "Snack Bar", "snackbar", world)
        
class CarrotStandTile(BuildingTile):
    def __init__(self, index, world):
        super(CarrotStandTile, self).__init__(index, "Carrot Stand", "carrotstand", world)
        
class CandyCartTile(BuildingTile):
    def __init__(self, index, world):
        super(CandyCartTile, self).__init__(index, "Cotton Candy Cart", "cottoncandymachine", world)

class Building(object):
    def __init__(self, index, entrance, world, size, tile_map, char_map, add_to_world=True):
        self.index = index
        self.entrance = (self.index[0] + entrance[0], self.index[1] + entrance[1])
        self.exit = self.entrance        
        self.rect = pg.Rect(world.grid[self.index].rect.topleft, size)
        self.tile_map = tile_map
        self.char_map = char_map
        self.windows = []
        
        self.assigned = []
        self.workers = []
        self.max_workers = 0
        self.patrons = []
        self.max_patrons = 0
        self.en_route_workers = []
        self.en_route_patrons = []
        self.outputs = {}
        self.inputs = {}
        
        if self.modes:
            self.mode_cycle = it.cycle(self.modes)
            self.mode = next(self.mode_cycle)
        
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
        if add_to_world:
            world.buildings.append(self)
        
        
    def has_patron_vacancies(self):
        return (len(self.en_route_patrons) + len(self.patrons) <
                                                                 self.max_patrons)
                                                                 
    def has_worker_vacancies(self):
        return (len(self.en_route_workers) + len(self.workers) <
                                                                 self.max_workers)
                                                                 
    def move(self, offset):
        self.rect.move_ip(offset)
        for tile in it.chain(self.tiles, self.windows):
            tile.rect.move_ip(offset)
    
    def update(self, world):
        for window in self.windows:
            window.update(world)
            
    def draw(self, surface):
        for window in self.windows:
            window.draw(surface, max([len(self.patrons), len(self.workers)]))
        for tile in self.tiles:
            tile.draw(surface)
       
class Warehouse(Building):
    footprint = (7, 6)
    size = (112, 112)
    name = "Warehouse"
    modes = None
    def __init__(self, index, world):
        tile_map =  ["XXXXXXX",
                          "OOOOOOO",
                          "OOOOOOO",
                          "OOOOOOO",
                          "OOOOOOO",
                          "OOOOOOO",
                          "WOOOOOO"]
        char_map = {"W": WarehouseTile}                  
        super(Warehouse, self).__init__(index, (2, 6), world,
                                                        self.size, tile_map, char_map)
        self.outputs = defaultdict(int)
        self.door_image = prepare.GFX["warehousedoor"]
        door_rect = self.door_image.get_rect(topleft=self.rect.topleft)
        self.door_rects = [door_rect.move(28, 96), door_rect.move(57, 96)]
        self.max_workers = 12

    def draw(self, surface):
        for window in self.windows:
            window.draw(surface, len(self.workers))
        for tile in self.tiles:
            tile.draw(surface)
        if not self.workers:
            for door_rect in self.door_rects:
                surface.blit(self.door_image, door_rect)
                
    def move(self, offset):
        self.rect.move_ip(offset)
        for dr in self.door_rects:
            dr.move_ip(offset)
        for tile in it.chain(self.tiles, self.windows):
            tile.rect.move_ip(offset)

 
class Tree(Building):
    footprint = (2, 1)
    size = (32, 32)
    name = "Tree"
    modes = None
    def __init__(self, index, world):
        tile_map = ["XX",
                          "TX"]
        char_map = {"T": TreeTile}
        super(Tree, self).__init__(index, (1, 1), world, self.size,
                                              tile_map, char_map)
        self.wood = 100
        self.max_workers = 1
        world.trees.append(self)
  
    def update(self, world):            
        if self.wood < 1:
            world.trees.remove(self)
            world.buildings.remove(self)
        
    def draw(self, surface):
        for tile in self.tiles:
            tile.draw(surface)
        
    def move(self, offset):
        self.rect.move_ip(offset)
        for tile in self.tiles:
            tile.rect.move_ip(offset)
            
    
class Ore(Building):
    footprint = (2, 1)
    size = (32, 32)
    name = "Iron Ore"
    modes = None
    def __init__(self, index, world):
        tile_map = ["XX",
                          "TX"]
        char_map = {"T": OreTile}
        super(Ore, self).__init__(index, (1, 0), world, self.size,
                                              tile_map, char_map, False)

        self.max_workers = 0
        world.ores.append(self)
  
    def update(self, world):            
        pass
        
    def draw(self, surface):
        for tile in self.tiles:
            tile.draw(surface)
        
    def move(self, offset):
        self.rect.move_ip(offset)
        for tile in self.tiles:
            tile.rect.move_ip(offset)
            


class Igloo(Building):
    footprint = (3, 3)
    size = (64, 48)
    name = "Igloo"
    modes = None
    def __init__(self, index, world):
        tile_map = ["OOOX",
                          "OOOX",
                          "IXXX"]
        char_map = {"I": IglooTile}
        super(Igloo, self).__init__(index, (1, 2), world, self.size,
                                               tile_map, char_map)
        world.grid[(self.index[0], self.index[1] + 2)].occupied = False
        self.windows = [Window((self.rect.left + 21, self.rect.top + 27),
                                             (11, 9))]
        self.max_patrons = 3
        world.rest_buildings.append(self)
            
            
class House(Building):
    footprint = (4, 4)
    size = (64, 80)
    name = "House"
    modes = None
    def __init__(self, index, world):
        tile_map = ["XXXX",
                          "OOOO",
                          "OOOO",
                          "OOOO",
                          "HOXO"]
        char_map = {"H": HouseTile}
        super(House, self).__init__(index, (2, 4), world, self.size,
                                                 tile_map, char_map)
        self.exit = (self.entrance[0], self.entrance[1] + 1)
        self.windows = [Window((self.rect.left + 11, self.rect.top + 53),
                                             (17, 18))]
        self.lights = HouseTreeLights((self.rect.left + 15, self.rect.top + 60))
        self.max_patrons = 6
        world.rest_buildings.append(self)
        
    def move(self, offset):
        self.rect.move_ip(offset)
        self.lights.rect.move_ip(offset)
        for tile in it.chain(self.tiles, self.windows):
            tile.rect.move_ip(offset)
        
    def update(self, world):
        for window in self.windows:
            window.update(world)
        self.lights.update(world)
    
    def draw(self, surface):
        for window in self.windows:
            window.draw(surface, len(self.patrons))
        for tile in self.tiles:
            tile.draw(surface)
        self.lights.draw(surface, len(self.patrons))
        

        
class GingerbreadHouse(Building):
    footprint = (5, 4)
    size = (80, 96)
    name = "Gingerbread House"
    modes = None
    def __init__(self, index, world):
        tile_map = ["XXXXX",
                           "XXXXX",
                           "OOOOO",
                           "OOOOO",
                           "OOOOO",
                           "GOOOO"]
        char_map = {"G": GingerHouseTile}
        super(GingerbreadHouse, self).__init__(index, (2, 5), world,
                                                                   self.size, tile_map, char_map)
        coords = [(16, 41), (16, 61), (34, 41), (52, 41), (52, 61)]
        self.window_spots = [(self.rect.left + x[0], self.rect.top + x[1]) for x in coords]
        self.windows = [Window(y, (10, 10)) for y in self.window_spots]
        self.window_images = it.cycle([prepare.GFX["candywindow" + str(z)] for z in range(1, 10)])
        self.window_image = next(self.window_images)
        self.dimmer = pg.Surface((10, 10)).convert_alpha()
        pg.draw.rect(self.dimmer, (0, 0, 0, 60), self.dimmer.get_rect().inflate(-2, -2))
        self.max_patrons = 8
        world.rest_buildings.append(self)
                                     
    def move(self, offset):
        self.rect.move_ip(offset)
        for tile in it.chain(self.tiles, self.windows):
            tile.rect.move_ip(offset)
        self.window_spots = [(x[0] + offset[0], x[1] + offset[1]) for x in self.window_spots]

        
        
    def update(self, world):
        if self.patrons and not world.ticks % 6:
            self.window_image = next(self.window_images)
        for window in self.windows:
            window.update(world)
        
    def draw(self, surface):
        for tile in self.tiles:
            tile.draw(surface)
        for window in self.windows:
            window.draw(surface, len(self.patrons))            
        for spot in self.window_spots:
            surface.blit(self.dimmer, spot)
            surface.blit(self.window_image, spot)

        
class Barn(Building):
    footprint = (7, 6)
    size = (112, 112)
    name = "Barn"
    modes = None
    def __init__(self, index, world):
        tile_map = ["XXXXXXX",
                          "OOOOOOO",
                          "OOOOOOO",
                          "OOOOOOO",
                          "OOOOOOO",
                          "OOOOOOO",
                          "BOOOOOO"]
        char_map = {"B": BarnTile}        
        super(Barn, self).__init__(index, (4, 6), world, self.size,
                                               tile_map, char_map)
        self.door_image = prepare.GFX["barndoor"]
        self.open_rect = self.door_image.get_rect(topleft=(self.rect.left + 38, self.rect.top + 41))
        self.shut_rect = self.door_image.get_rect(topleft=(self.rect.left + 49, self.rect.top + 41))
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
        for r in [self.rect, self.deer_rect,
                     self.open_rect, self.shut_rect]:
            r.move_ip(offset)
        for tile in it.chain(self.tiles, self.reindeers):
            tile.rect.move_ip(offset)    
    
    def draw(self, surface):
        for tile in self.tiles:
            tile.draw(surface)
        if self.workers:
            #surface.blit(self.open_door, self.door_rect)
            surface.blit(self.door_image, self.open_rect)
        else:
            #surface.blit(self.shut_door, self.door_rect)
            surface.blit(self.door_image, self.shut_rect)
        for reindeer in self.reindeers:
            reindeer.draw(surface)        


class Bakery(Building):
    footprint = (4, 3)
    size = (64, 48)
    name = "Bakery"
    modes = ["Cookies", "Carrot Cake"]
    def __init__(self, index, world):
        tile_map = ["OOOO",
                          "OOOO",
                          "BOOO"]
        char_map = {"B": BakeryTile}        
        super(Bakery, self).__init__(index, (2, 2), world, self.size,
                                               tile_map, char_map)
        self.outputs["Cookies"] = 0
        self.outputs["Carrot Cake"] = 0
        self.inputs["Carrot"] = 0
        self.inputs["Sugar"] = 100
        self.max_workers = 2
        self.windows = [Window((self.rect.left + 11, self.rect.top + 21),
                                             (51, 16))]
        
    def update(self, world):
        for worker in self.workers:
            if self.mode == "Cookies":
                if self.inputs["Sugar"] >= .01:
                    self.outputs["Cookies"] += .02 * worker.skills["Baking"] 
                    self.inputs["Sugar"] -= .01
            elif self.mode == "Carrot Cake":
                if (self.inputs["Sugar"] >= .005 and self.inputs["Carrots"] >= .01):
                    self.outputs["Carrot Cake"] += .02 * worker.skills["Baking"]
                    self.inputs["Sugar"] -= .005
                    self.inputs["Carrot"] -= .01
                        
        for window in self.windows:
            window.update(world)        

    def move(self, offset):
        self.rect.move_ip(offset)
        for tile in it.chain(self.tiles, self.windows):
            tile.rect.move_ip(offset)   
    
    def draw(self, surface):
        for window in self.windows:
            window.draw(surface, len(self.workers))
        for tile in self.tiles:
            tile.draw(surface)
        
            
class MossFarm(Building):
    footprint = (4, 4)
    size = (64, 80)
    name = "Moss Farm"
    frame = prepare.GFX["farmframe"]
    modes = None
    def __init__(self, index, world):
        tile_map = ["XXXX",
                          "OOMM",
                          "SOMM",
                          "MMMM",
                          "MMMM"]
        char_map = {"M": MossTile,
                             "S": PottingShed}
        super(MossFarm, self).__init__(index, (0, 2), world,
                                                      self.size, tile_map, char_map)
        self.exit = (self.entrance[0] - 1, self.entrance[1])
        self.windows = [Window((self.rect.left + 9, self.rect.top + 18), (7, 7))]
        self.growth = 0
        self.current_growth = 0
        self.outputs["Moss"] = 0
        self.max_workers = 2
        
    def update(self, world):
        for window in self.windows:
            window.update(world)
        for worker in self.workers:
            self.growth += 1 *  worker.skills["Farming"]
            self.current_growth += 1 *  worker.skills["Farming"]
        if self.current_growth > 300:
            self.current_growth -= 300
            for tile in self.tiles:
                try:
                    tile.image = next(tile.images)
                except AttributeError:
                    pass
        if self.growth > 1500:
            self.outputs["Moss"] += 100
            self.growth = 0
            self.currrent_growth = 0
            
    def draw(self, surface):
        for window in self.windows:
            window.draw(surface, len(self.workers))
        for tile in self.tiles:
            tile.draw(surface)
        surface.blit(self.frame, (self.rect.left, self.rect.top + 16))


class CarrotFarm(Building):
    footprint = (4, 4)
    size = (64, 80)
    name = "Carrot Farm"
    frame = prepare.GFX["farmframe"]
    modes = None
    def __init__(self, index, world):
        tile_map = ["XXXX",
                          "OOCC",
                          "SOCC",
                          "CCCC",
                          "CCCC"]
        char_map = {"C": CarrotTile,
                             "S": PottingShed}
        super(CarrotFarm, self).__init__(index, (0, 2), world,
                                                        self.size, tile_map, char_map)
        self.exit = (self.entrance[0] - 1, self.entrance[1])
        self.windows = [Window((self.rect.left + 9, self.rect.top + 18), (7, 7))]
        self.growth = 0
        self.current_growth = 0
        self.outputs["Carrot"] = 0
        self.max_workers = 2
        
    def update(self, world):
        for window in self.windows:
            window.update(world)
        for worker in self.workers:
            self.growth += 1 * worker.skills["Farming"]
            self.current_growth += 1 * worker.skills["Farming"]
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
            
    def draw(self, surface):
        for window in self.windows:
            window.draw(surface, len(self.workers))
        for tile in self.tiles:
            tile.draw(surface)
        surface.blit(self.frame, (self.rect.left, self.rect.top + 16))


class BeetFarm(Building):
    footprint = (4, 4)
    size = (64, 80)
    name = "Beet Farm"
    frame = prepare.GFX["farmframe"]
    modes = None
    def __init__(self, index, world):
        tile_map = ["XXXX",
                          "OOBB",
                          "SOBB",
                          "BBBB",
                          "BBBB"]
        char_map = {"B": BeetTile,
                             "S": PottingShed}
        super(BeetFarm, self).__init__(index, (0, 2), world,
                                                        self.size, tile_map, char_map)
        self.exit = (self.entrance[0] - 1, self.entrance[1])
        self.windows = [Window((self.rect.left + 9, self.rect.top + 18), (7, 7))]
        self.growth = 0
        self.current_growth = 0
        self.outputs["Sugar"] = 0
        self.max_workers = 2
        
    def update(self, world):
        for window in self.windows:
            window.update(world)
        for worker in self.workers:
            self.growth += 1 * worker.skills["Farming"] #TODO: should be from elf skill and use growth stages not modulo
            self.current_growth += 1 * worker.skills["Farming"]
        if self.current_growth > 300:
            self.current_growth -= 300
            for tile in self.tiles:
                try:
                    tile.image = next(tile.images)
                except AttributeError:
                    pass                
        if self.growth > 1500:
            self.outputs["Sugar"] += 100
            self.growth = 0
            self.current_growth = 0
            
    def draw(self, surface):
        for window in self.windows:
            window.draw(surface, len(self.workers))
        for tile in self.tiles:
            tile.draw(surface)
        surface.blit(self.frame, (self.rect.left, self.rect.top + 16))

class WoodShed(Building):
    footprint = (2, 2)
    size = (32, 32)
    name = "Wood Shed"
    frame = prepare.GFX["farmframe"]
    modes = None
    def __init__(self, index, world):
        tile_map = ["OX",
                          "WO"]
        char_map = {"W": WoodShedTile}
        super(WoodShed, self).__init__(index, (0, 1), world,
                                                       self.size, tile_map, char_map)
        self.exit = (self.entrance[0] - 1, self.entrance[1])
        self.outputs["Wood"] = 0
        self.max_workers = 4
        
        
class Mine(Building):
    footprint = (2, 2)
    size = (32, 32)
    name = "Mine"
    modes = None
    def __init__(self, index, world):
        tile_map = ["OX",
                          "WO"]
        char_map = {"W": MineTile}
        super(Mine, self).__init__(index, (0, 1), world,
                                               self.size, tile_map, char_map)
        self.exit = (self.entrance[0], self.entrance[1] + 1)
        self.outputs["Iron"] = 0
        self.max_workers = 4
        
    def update(self, world):
        for worker in self.workers:
            self.outputs["Iron"] += .005 * worker.skills["Mining"]

            
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
    
    def draw(self, surface):
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
            
    def draw(self, surface):
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
    footprint = (10, 3)
    size = (160, 48)
    name = "Snow Forts"
    modes = None
    def __init__(self, index, world):
        tile_map = ["OOOOOOOOOO",
                          "XOOOOOOOOO", 
                          "FOOOOOOOOO"]
        char_map = {"F": FortsTile}
        super(SnowForts, self).__init__(index, (0, 1), world,
                                                       self.size, tile_map, char_map)
        self.exit = (self.entrance[0] - 1, self.entrance[1])
        self.throwers = [LeftThrower(self, (self.rect.left + 37,
                                                           self.rect.top + 24)), 
                                RightThrower(self, (self.rect.left + 115,
                                                             self.rect.top + 24))]
        self.snowballs = []
        self.max_patrons = 8
        world.cheer_buildings.append(self)
        
    def update(self, world):
        if self.patrons:
            for elem in it.chain(self.throwers, self.snowballs):
                elem.update(world)
            
    def move(self, offset):
        self.rect.move_ip(offset)
        for elem in it.chain(self.tiles, self.throwers, self.snowballs):
            elem.rect.move_ip(offset)

    def give_cheer(self, elf):
        if len(self.patrons) > 1:
            elf.cheer += 1.5
            elf.energy -= .5
    
    def draw(self, surface):
        for tile in self.tiles:
            tile.draw(surface)
        if len(self.patrons) > 1:
            for elem in it.chain(self.throwers, self.snowballs):
                elem.draw(surface)
                
                
class Theater(Building):
    footprint = (3, 3)
    size = (48, 64)
    name = "Theater"
    modes = None
    def __init__(self, index, world):
        tile_map = ["XXX",
                          "OOO",
                          "OOO", 
                          "TOO"]
        char_map = {"T": TheaterTile}
        super(Theater, self).__init__(index, (0, 3), world,
                                                   self.size, tile_map, char_map)
        self.exit = (self.entrance[0] - 1, self.entrance[1])
        puppets1 = [prepare.GFX["puppet" + str(x)] for x in range(1, 5)]
        puppets = [prepare.GFX["puppet" + str(x)] for x in range(1, 18)]
        puppets1.extend(puppets)
        self.puppet_images = it.cycle(puppets1)
        self.puppet_image = next(self.puppet_images)
        self.curtain_image = prepare.GFX["curtain"]
        self.patron_image = prepare.GFX["showpatron"]
        self.stage_rect = pg.Rect(self.rect.left + 17, self.rect.top + 25, 14, 9)
        patron_offsets = [(22, 40), (14, 50), (31, 40), (29, 50), (13, 40), (21, 50)]
        self.patron_rects = [pg.Rect(self.rect.left + x[0], self.rect.top + x[1], 5, 14) for x in patron_offsets]
        self.in_use = 0
        self.max_patrons = 6
        world.cheer_buildings.append(self)
        
    def update(self, world):
        if self.patrons:
            if not world.ticks % 7:
                self.puppet_image = next(self.puppet_images)
        
    def move(self, offset):
        self.rect.move_ip(offset)
        self.stage_rect.move_ip(offset)
        for prect in self.patron_rects:
            prect.move_ip(offset)
        for tile in self.tiles:
            tile.rect.move_ip(offset)

    def give_cheer(self, elf):
        elf.cheer += 1
        elf.energy += .3
    
    
    def draw(self, surface):
        for tile in self.tiles:
            tile.draw(surface)
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
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)

        
class SkatingRink(Building):
    footprint = (12, 5)
    size = (192, 80)
    name = "Skating Rink"
    modes = None
    def __init__(self, index, world):
        tile_map = ["OOOOOOOOOOOO",
                          "OOOOOOOOOOOO",
                          "OOOOOOOOOOOO",
                          "OOOOOOOOOOOO", 
                          "ROOOOOOOOOOO"]
        char_map = {"R": RinkTile}
        super(SkatingRink, self).__init__(index, (9, 0),
                                                         world, self.size, tile_map,
                                                         char_map)
        self.exit = (self.entrance[0], self.entrance[1] - 1)
        self.rink_rect = pg.Rect(self.rect.left + 18, self.rect.top, 152, 68) 
        self.skaters = []
        self.max_patrons = 10
        world.cheer_buildings.append(self)
        
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
        self.rink_rect.move_ip(offset)
        for tile in self.tiles:
            tile.rect.move_ip(offset)
        for skater in self.skaters:
            skater.rect.move_ip(offset)

    def give_cheer(self, elf):
        elf.cheer += 2.5
        elf.energy += 1
        
    def draw(self, surface):
        for tile in self.tiles:
            tile.draw(surface)
        for skater in self.skaters:
            skater.draw(surface)

class SnackBar(Building):
    footprint = (4, 3)
    size = (64, 64)
    name = "Snack Bar"
    modes = ["Cookies", "Carrot Cake"]
    def __init__(self, index, world):
        tile_map = ["XXXX",
                          "OOOO",
                          "OOOO", 
                          "BOOO"]
        char_map = {"B": SnackBarTile}
        super(SnackBar, self).__init__(index, (0, 2), world,
                                                      self.size, tile_map, char_map)
        self.exit = (self.entrance[0] - 1, self.entrance[1])
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
        self.inputs["Carrot Cake"] = 0
        self.inputs["Cookies"] = 0
        world.food_buildings.append(self)
    
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
        for patron in self.patrons:
            milk = False
            food_value = 0
            cavities = 0
            if self.inputs["Milk"]:
                    self.inputs["Milk"] -= .01
                    food_value += 1
                    milk = True
            if self.mode == "Cookies" and self.inputs["Cookies"] >= .01:
                self.inputs["Cookies"] -= .01
                food_value += 2
                if milk:
                    food_value += .5
                cavities += .2
            elif self.mode == "Carrot Cake" and self.inputs["Carrot Cake"] >= .01:    
                self.inputs["Carrot Cake"] -= .01
                food_value += 1.5
                if milk:
                    food_value += .4
                cavities += .75
                
            patron.food += food_value
            patron.cavities -= cavities
            
    def draw(self, surface):
        for tile in self.tiles:
            tile.draw(surface)
        for patron_rect in self.patron_rects:
            surface.blit(self.patron_images[patron_rect[1]], 
                             (self.rect.left + patron_rect[0],
                             self.rect.top + patron_rect[1]))
                             
                    
class CarrotStand(Building):
    footprint = (1, 1)
    size = (32, 48)
    name = "Carrot Stand"
    modes = None
    def __init__(self, index, world):
        tile_map = ["XX",
                          "XX", 
                          "BX"]
        char_map = {"B": CarrotStandTile}
        super(CarrotStand, self).__init__(index, (1, 2),
                                                         world, self.size, tile_map,
                                                         char_map)
        self.food_rect = pg.Rect(self.rect.left - 32, self.rect.top, 96, 96)
        self.inputs["Carrot"] = 10
        
    def move(self, offset):
        self.rect.move_ip(offset)
        self.food_rect.move_ip(offset)
        for tile in self.tiles:
            tile.rect.move_ip(offset)
        
    def update(self, world):
        elves = world.elves
        for elf in [x for x in elves if x.rect.colliderect(self.food_rect)]:
            if self.inputs["Carrot"] >= .2:
                elf.food += .2
                self.inputs["Carrot"] -= .2
                if elf.food > elf.max_food:
                    elf.food = elf.max_food

                    
class CottonCandyCart(Building):
    footprint = (1, 1)
    size = (32, 32)
    name = "Cotton Candy Cart"
    modes = None
    def __init__(self, index, world):
        tile_map = ["XX", 
                          "CX"]
        char_map = {"C": CandyCartTile}
        super(CottonCandyCart, self).__init__(index, (1, 1),
                                                         world, self.size, tile_map,
                                                         char_map)
        self.food_rect = pg.Rect(self.rect.left - 32, self.rect.top, 96, 96)
        self.inputs["Sugar"] = 0
        
    def move(self, offset):
        self.rect.move_ip(offset)
        self.food_rect.move_ip(offset)
        for tile in self.tiles:
            tile.rect.move_ip(offset)
        
    def draw(self, surface):
        for tile in self.tiles:
            tile.draw(surface)
        
    def update(self, world):
        elves = world.elves
        for elf in [x for x in elves if x.rect.colliderect(self.food_rect)]:
            if self.inputs["Sugar"] >= .1:
                elf.food += .05
                elf.cheer += .1
                self.inputs["Sugar"] -= .1
                elf.food = max(elf.food, elf.max_food)
                elf.cheer = max(elf.cheer, elf.max_cheer)
                             
     