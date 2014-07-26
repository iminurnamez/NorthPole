import itertools as it
from collections import defaultdict
import pygame as pg
from .. import prepare
from .buildings import Building, PottingShed, Tree, Window

class PlantSpot(object):
    def __init__(self, index, world):
        self.index = index
        self.rect = pg.Rect((0, 0), (32, 32))
        self.rect.bottomleft = world.grid[self.index].rect.bottomleft
        self.occupant = Sapling(self.rect, world)

    def move(self, offset):
        self.rect.move_ip(offset)

    def draw(self, surface):
        if self.occupant.name == "Sapling":
            self.occupant.draw(surface)
            
    def update(self, num_workers, world):
        plant = self.occupant
        if plant.name == "Sapling":
            plant.update(num_workers)
            if plant.grown:
                self.occupant = Tree((self.index[0], self.index[1] - 1), world)

        else:
            if plant.wood <= 0:
                self.occupant = Sapling(self, world)


class Sapling(object):
    name = "Sapling"
    def __init__(self, rect, world):
        self.grown = False
        self.growth = 0
        self.growth_stage = 1
        self.rect = rect
        self.image = prepare.GFX["sapling" + str(self.growth_stage)]

    def update(self, num_workers):
        self.growth += num_workers * 1
        if self.growth > 1000:
            self.growth -= 1000
            self.growth_stage += 1
            try:
                self.image = prepare.GFX["sapling" + str(self.growth_stage)]
            except KeyError:
                pass
        if self.growth_stage > 4:
            self.grown = True

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Nursery(Building):
    size = (96, 112)
    footprint = (6, 6)
    name = "Nursery"
    modes = None
    def __init__(self, index, world):
        tile_map = ["XXXXXX",
                          "OXOXOX",
                          "XXOOOX",
                          "OXOOOO",
                          "XXOOOX",
                          "OXPOOX",
                          "XXOXOX"]
        char_map = {"P": PottingShed}
        super(Nursery, self).__init__(index, (5, 4), world,
                                                   self.size, tile_map, char_map)
        self.windows = [Window((self.rect.left + 41, self.rect.top + 66), (7, 7))]
        self.outputs = defaultdict(int)
        self.max_workers = 2
        spots = [(0, 1), (2, 1), (4, 1), (0, 3), (5, 3), (0, 5), (2, 6), (4, 6)] 
        self.spots = [PlantSpot((self.index[0] + spot[0], self.index[1] + spot[1]), world)
                            for spot in spots]

    def update(self, world):
        for window in self.windows:
            window.update(world)
        for spot in self.spots:
            spot.update(len(self.workers), world)

    def draw(self, surface):        
        for window in self.windows:
            window.draw(surface, max([len(self.patrons), len(self.workers)]))
        for tile in self.tiles:
            tile.draw(surface)
        for spot in self.spots:
            spot.draw(surface)

    def move(self, offset):
        self.rect.move_ip(offset)
        for tile in it.chain(self.tiles, self.windows):
            tile.rect.move_ip(offset)
        for spot in self.spots:
            spot.move(offset)
