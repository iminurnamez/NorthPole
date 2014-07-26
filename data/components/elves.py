import random
import pygame as pg
import itertools as it
from collections import OrderedDict
from .. import prepare
from . import elfnames

                                  
def name_generator(first_names, last_names=None):
    name = random.choice(first_names)
    if last_names:
        name += " " + random.choice(last_names)
    return name
    
    
class Elf(object):
    def __init__(self, index, world):
        self.index = index
        self.rect = pg.Rect(world.grid[index].rect.topleft, (16, 16))
        self.sex = random.choice(("Male", "Female"))
        if self.sex == "Male":
            self.name = name_generator(elfnames.MALE, elfnames.LAST)
        else:
            self.name = name_generator(elfnames.FEMALE, elfnames.LAST)        
        self.max_energy = 1000.0  #random.randint(800, 1000)
        self.max_cheer = 1000.0  #random.randint(800, 1000)
        self.max_food = 1000.0  #random.randint(800, 1000)
        self.max_cavities = 1000.0
        self.energy = self.max_energy * .2
        self.cheer = self.max_cheer * .5
        self.food = self.max_food * .5
        self.cavities = self.max_cavities
        self.stats = {"Wits": .5, # + skill acquisition
                           "Mirth": .5,  #max_cheer
                           "Stamina": .5, #max_energy
                           "Strength": .5, #max_cargo
                           "Charm": .5}# + for reindeer handlers/donation army
        
                
        self.skills = OrderedDict([("Farming", random.uniform(.25, .75)),
                                              ("Logging", random.uniform(.25, .75)),
                                              ("Mining", random.uniform(.25, .75)),
                                              ("Hauling", random.uniform(.25, .75)),
                                              ("Husbandry", random.uniform(.25, .75)),
                                              ("Baking", random.uniform(.25, .75)),
                                              ("Woodworking", random.uniform(.25, .75)),
                                              ("Metalworking", random.uniform(.25, .75)),
                                              ("Stitchery", random.uniform(.25, .75))])
                           
                           
                          
                            
                             
        self.state = "Idle"
        self.speed = 1
        self.x_velocity = 0
        self.y_velocity = 0
        self.cargo = None
        self.goal = None
        self.destination = None
        self.home = None
        self.job = None
        self.venue = None
        self.images = {"Travelling": {(-1, -1): it.cycle([prepare.GFX["elfleftwalk1"],
                                                                         prepare.GFX["elfleftwalk2"]]),
                                               (-1, 0): it.cycle([prepare.GFX["elfleftwalk1"],
                                                                        prepare.GFX["elfleftwalk2"]]),
                                               (-1, 1): it.cycle([prepare.GFX["elfleftwalk1"],
                                                                        prepare.GFX["elfleftwalk2"]]),
                                               (0, -1): it.cycle([prepare.GFX["elfupwalk1"],
                                                                        prepare.GFX["elfupwalk2"]]),
                                               (0, 0): it.cycle([prepare.GFX["elfleftwalk1"]]),
                                               (0, 1): it.cycle([prepare.GFX["elfdownwalk1"],
                                                                       prepare.GFX["elfdownwalk2"]]),
                                               (1, -1): it.cycle([prepare.GFX["elfrightwalk1"],
                                                                        prepare.GFX["elfrightwalk2"]]),
                                               (1, 0): it.cycle([prepare.GFX["elfrightwalk1"],
                                                                       prepare.GFX["elfrightwalk2"]]),
                                               (1, 1): it.cycle([prepare.GFX["elfrightwalk1"],
                                                                       prepare.GFX["elfrightwalk2"]])},
                               "Hauling": {(-1, -1): it.cycle([prepare.GFX["elfleft1"],
                                                                         prepare.GFX["elfleft2"]]),
                                               (-1, 0): it.cycle([prepare.GFX["elfleft1"],
                                                                        prepare.GFX["elfleft2"]]),
                                               (-1, 1): it.cycle([prepare.GFX["elfleft1"],
                                                                        prepare.GFX["elfleft2"]]),
                                               (0, -1): it.cycle([prepare.GFX["elfup1"],
                                                                        prepare.GFX["elfup2"]]),
                                               (0, 0): it.cycle([prepare.GFX["elfleft1"]]),
                                               (0, 1): it.cycle([prepare.GFX["elfdown1"],
                                                                       prepare.GFX["elfdown2"]]),
                                               (1, -1): it.cycle([prepare.GFX["elfright1"],
                                                                        prepare.GFX["elfright2"]]),
                                               (1, 0): it.cycle([prepare.GFX["elfright1"],
                                                                       prepare.GFX["elfright2"]]),
                                               (1, 1): it.cycle([prepare.GFX["elfright1"],
                                                                       prepare.GFX["elfright2"]])},
                               "Logging": it.cycle([prepare.GFX["chop3"],
                                                            prepare.GFX["chop1"],
                                                            prepare.GFX["chop2"],
                                                            prepare.GFX["chop1"],
                                                            prepare.GFX["chop3"]]),
                               "Idle": it.cycle([prepare.GFX["elfleftidle1"], 
                                                       prepare.GFX["elfleftidle2"]])}
        
        self.image = next(self.images[self.state])
        
    def move(self, offset):
        self.rect.move_ip(offset)

    def update_image(self, world):
        if not world.ticks % 3 and self.state in {"Travelling", "Hauling"}:
            self.image = next(self.images[self.state][(self.x_velocity, self.y_velocity)])
        elif not world.ticks % 5 and self.state == "Idle":
            self.image = next(self.images["Idle"])
            
    def draw(self, surface):
        if self.state in {"Travelling", "Hauling", "Logging", "Mining", "Idle"}:
            surface.blit(self.image, self.rect)           
        
    def travel(self, world):
        self.x_velocity = 0
        self.y_velocity = 0
        if self.rect.centerx < world.grid[self.destination].rect.centerx:
            self.x_velocity = 1
        elif self.rect.centerx > world.grid[self.destination].rect.centerx:
            self.x_velocity = -1
        elif self.rect.centery < world.grid[self.destination].rect.centery:
            self.y_velocity = 1
        elif self.rect.centery > world.grid[self.destination].rect.centery:
            self.y_velocity = -1        
        self.move((self.x_velocity, self.y_velocity))
       
    def find_path(self, world):
        the_world = world
        grid = world.grid
        
        #depth = (abs(self.goal[0] - self.index[0]) + abs(self.goal[1] - self.index[1])) * 2
        neighbors = []
        visited = set()
        neighbors.append([self.index])
        visited.add(self.index)
        goal_found = False
        i = 0
        while not goal_found:
        #for i in range(1, depth + 1):
            i += 1
            more_neighbors = set()
            for a_neighbor in neighbors[i - 1]:
                for next_neighbor in grid[a_neighbor].get_open_neighbors(the_world):
                    if next_neighbor in visited:
                        pass
                    elif grid[next_neighbor].occupied:
                        visited.add(next_neighbor)
                    elif next_neighbor == self.goal:
                        visited.add(next_neighbor)
                        more_neighbors.add(next_neighbor)
                        goal_found = True
                        break
                    elif next_neighbor not in more_neighbors:
                        more_neighbors.add(next_neighbor)
                        visited.add(next_neighbor)
            neighbors.append(more_neighbors)
            if goal_found:
                break
            #just in case
            if i > 1000:
                print "Depth greater than 1000 in find_path"
                print self.name
                print self.destination
                print self.venue
                break            
        reverse_route = []
        best_landing_spot = list(neighbors[len(neighbors) - 1])[0]
        for neighbor in neighbors[len(neighbors) - 1]:
            distance = abs(neighbor[0] - self.goal[0]) + abs(neighbor[1] - self.goal[1])
            best_distance = abs(best_landing_spot[0] - self.goal[0]) + abs(best_landing_spot[1] - self.goal[1])
            if distance < best_distance:
                best_landing_spot = neighbor
            elif distance == best_distance and random.choice([True, False]):
                best_landing_spot = neighbor

        i = 0
        while i < len(neighbors):
            reverse_route.append(best_landing_spot)
            candidates = []
            for some_neighbor in grid[best_landing_spot].get_open_neighbors(the_world):
                if some_neighbor in neighbors[len(neighbors) -1 - (i + 1)]:
                    candidates.append(some_neighbor)
            
            # Bug alerter - shouldn't need try/except
            try:
                new_landing_spot = candidates[0]
            
            except IndexError:
                print "Job: {}".format(self.job)
                print "Index: {}".format(self.index)
                print "Goal: {}".format(self.goal)
                print "Venue: {}".format(self.venue.name)
                print "Entrance: {}".format(self.venue.entrance)
                print "State: {} {}".format(self.state, self.next_state)
                print "Cargo: {}".format(self.cargo)
                print "E: {}".format(self.energy)
                print "F: {}".format(self.food)
                print "C: {}".format(self.cheer)
                
                
            
            for candidate in candidates:
                potential_best_dist = (abs(candidate[0] - self.goal[0]) +
                                                 abs(candidate[1] - self.goal[1]))
                now_best_dist = (abs(new_landing_spot[0] - self.goal[0]) +
                                           abs(new_landing_spot[1] - self.goal[1]))
                if potential_best_dist < now_best_dist:
                    new_landing_spot = candidate
            best_landing_spot = new_landing_spot
            if best_landing_spot == self.index:
                return reverse_route[::-1]
            i += 1
        return reverse_route[::-1]
                
    def assign_job(self, building, world):
        if self.job is not None:
            self.job.assigned.remove(self)
            if self in self.job.workers:
                self.job.workers.remove(self)
            if self in self.job.en_route_workers:
                self.job.en_route_workers.remove(self)
            if self.venue:
                if self in self.venue.workers:
                    self.venue.workers.remove(self)
                if self in self.venue.en_route_workers:
                    self.venue.en_route_workers.remove(self)
            if self.state in ("Working", "Hauling", "Logging"):
                self.index = self.job.exit
                self.rect.center = world.grid[self.index].rect.center
                self.state = "Idle"
        self.job = building
        self.job.assigned.append(self)
        self.cargo = None
        
        
    def work_check(self, world):
        if (self.energy < 200 or
                    self.food < 150 or
                    self.cheer < 100):
            self.state = "Idle"
            try:
                self.job.workers.remove(self)
            except ValueError as e:
                print e
                print "Elf not in elf.job.workers"
            self.index = self.job.exit
            self.rect.center = world.grid[self.index].rect.center
            return True
    
    def do_work(self, world):
        # TODO - work should be incremented by skill check not a number    
        if self.job.name == "Wood Shed":
            if self.index == self.job.entrance:
                if self.cargo:
                    self.job.outputs[self.cargo[0]] += self.cargo[1]
                if self.work_check(world):
                    return
                open_trees = [x for x in world.trees if not x.workers + x.en_route_workers] 
                tree = min(open_trees, key=lambda x: (abs(x.index[0] - self.index[0]) +
                                                                  abs(x.index[1] - self.index[1])))
                self.venue = tree
                self.venue.en_route_workers.append(self)
                self.goal = self.venue.entrance
                self.state = "Travelling"
                self.next_state = "Logging"
                self.cargo = ("Wood", 0)
                self.path = iter(self.find_path(world))
                self.destination = next(self.path)
                                
        elif self.job.name == "Schoolhouse":
            if self.work_check(world):
                return
            self.energy -= .5
            self.food -= .5
            self.cheer -= .6
            
        elif self.job.name == "Warehouse":
            if self.work_check(world):
                return
            max_load = (self.stats["Strength"] + self.skills["Hauling"]) * 100
            if self.index == self.job.entrance:
                big_stock = ("", 0)
                stock_place = None
                big_need = ("", 500)
                need_place = None
                for building in [x for x in world.buildings if x != self.job]:
                    for stock in building.outputs:
                        if building.outputs[stock] > big_stock[1]:
                            big_stock = (stock, building.outputs[stock])
                            stock_place = building
                    for need in building.inputs:
                        if (1000 - building.inputs[need] > big_need[1] and 
                                                             self.job.outputs[need] > 0):
                            big_need = (need, 1000 - building.inputs[need])
                            need_place = building
                if need_place or stock_place:
                    if not need_place or big_stock[1] > big_need[1]:
                        self.venue = stock_place
                        for thing in stock_place.inputs:
                            if stock_place.inputs[thing] < 500 and self.job.outputs[thing] > 0:
                                amt = min(max_load, self.job.outputs[thing],
                                                 1000 - stock_place.inputs[thing])
                                self.job.outputs[thing] -= amt
                                self.cargo = (thing, amt)
                                break
                    else:
                        self.venue = need_place
                        self.cargo = (big_need[0], min(max_load,
                                            self.job.outputs[big_need[0]], big_need[1]))
                    if self.cargo:
                        self.job.outputs[self.cargo[0]] -= self.cargo[1]
                    self.goal = self.venue.entrance
                    self.state = "Hauling"
                    self.next_state = "Working"
                    self.path = iter(self.find_path(world))
                    self.destination = next(self.path)   

        else:    
            if self.work_check(world):
                return
            self.energy -= 1
            self.food -= 1
            self.cheer -= 1    

    def update(self, world):
        self.energy = max(1, min(self.energy, self.max_energy))
        self.cheer = max(1, min(self.cheer, self.max_cheer))
        self.food = max(1, min(self.food, self.max_food))
     
        if self.state == "Idle":
            if (self.energy > self.max_energy * .7 
                        and self.food > self.max_food * .7
                        and self.cheer > self.max_cheer * .7
                        and self.cavities > self.max_cavities * .3
                        and ((self.job is not None) and self.job.has_worker_vacancies())):
                self.state = "Travelling"
                self.next_state = "Working"
                self.venue = self.job
                self.goal = self.venue.entrance
                self.venue.en_route_workers.append(self)
                self.path = iter(self.find_path(world))
                self.destination = next(self.path)
                
            else:    
                desires = {"Resting": (self.max_energy / self.energy),
                                "Merrymaking": (self.max_cheer / self.cheer),
                                "Eating": (self.max_food / self.food),
                                "Cavities": (self.max_cavities / self.cavities)}           
                top_desires = iter(sorted(desires, key=desires.get, reverse=True))
                top_desire = next(top_desires)           
                open_cheer_buildings = [x for x in world.cheer_buildings if x.has_patron_vacancies()]
                open_food_buildings = [x for x in world.food_buildings if x.has_patron_vacancies()]
                open_rest_buildings = [x for x in world.rest_buildings if x.has_patron_vacancies()]
                open_dental_buildings = [x for x in world.dental_buildings if x.has_patron_vacancies()]
                desire_venues = {"Resting": None,
                                           "Merrymaking": None,
                                           "Eating": None,
                                           "Cavities": None}
                if open_dental_buildings and self.cavities < self.max_cavities * .8:
                    desire_venues["Cavities"] = random.choice(open_dental_buildings)
                if open_rest_buildings and self.energy < self.max_energy:
                    desire_venues["Resting"] = random.choice(open_rest_buildings)
                if open_cheer_buildings and self.cheer < self.max_cheer:
                    desire_venues["Merrymaking"] = random.choice(open_cheer_buildings)
                if open_food_buildings and self.food < self.max_food:
                    desire_venues["Eating"] = random.choice(open_food_buildings)
                if not any([desire_venues["Resting"], desire_venues["Merrymaking"],
                                 desire_venues["Eating"], desire_venues["Cavities"]]):
                    return                             
                while True:
                    if desire_venues[top_desire]:
                        break
                    else:
                        try:
                            top_desire = next(top_desires)
                        except StopIteration:
                            return
                
                self.state = "Travelling"
                self.next_state = top_desire
                self.venue = desire_venues[top_desire]
                self.venue.en_route_patrons.append(self)
                self.goal = self.venue.entrance
                self.path = iter(self.find_path(world))
                self.destination = next(self.path)
            
        elif self.state == "Resting":
            if self.energy >= self.max_energy:
                self.energy = self.max_energy
                self.state = "Idle"
                self.venue.patrons.remove(self)
                self.index = self.venue.exit
                self.rect.center = world.grid[self.index].rect.center
            else:
                if self.energy < self.max_energy / 3:
                    self.energy += 1
                elif self.energy < self.max_energy / 2:
                    self.energy += 2
                else:
                    self.energy += 3
                
        elif self.state == "Cavities":
            if self.cavities >= self.max_cavities:
                self.cavities = self.max_cavities
                self.state ="Idle"
                self.venue.patrons.remove(self)
                self.index= self.venue.exit
                self.rect.center = world.grid[self.index].rect.center
                
        elif self.state == "Working":
            self.do_work(world)
            
        elif self.state == "Eating":
            if self.food >= self.max_food:
                self.venue.patrons.remove(self)
                self.food = self.max_food
                self.state = "Idle"
                self.index = self.venue.exit
                self.rect.center = world.grid[self.index].rect.center             

        elif self.state == "Merrymaking":
            if self.cheer >= self.max_cheer:
                self.venue.patrons.remove(self)
                self.cheer = self.max_cheer
                self.state = "Idle"
                self.index = self.venue.exit
                self.rect.center = world.grid[self.index].rect.center
            else:
                self.venue.give_cheer(self)

      
        elif self.state == "Logging":
            if not world.ticks % 7:
                self.image = next(self.images["Logging"])
            how_much_wood = .02 * self.skills["Logging"]
            self.cargo = ("Wood", self.cargo[1] + how_much_wood)
            self.venue.wood -= how_much_wood
            self.energy -= 1
            self.cheer -= 1
            self.food -= 1
            if (self.energy < 200
                 or self.food < 150
                 or self.cheer < 100
                 or self.cargo[1] > self.stats["Strength"] * 100):
                self.venue.workers.remove(self)
                self.state = "Travelling"
                self.next_state = "Working"
                self.venue = self.job
                self.venue.en_route_workers.append(self)
                self.goal = self.venue.entrance
                self.path = iter(self.find_path(world))
                self.destination = next(self.path)
   
        elif self.state == "Hauling":
            self.energy -= 1
            self.cheer -= 1
            self.food -= 1
            max_load = (self.stats["Strength"] + self.skills["Hauling"]) * 100
            if self.rect.topleft == world.grid[self.goal].rect.topleft:
                self.index = self.goal
                if self.index == self.job.entrance:
                    if self.cargo:
                        self.job.outputs[self.cargo[0]] += self.cargo[1]
                        self.cargo = None
                    if self.work_check(world):
                        return    
                    self.state = "Working"
                else:
                    if self.cargo:
                        self.venue.inputs[self.cargo[0]] += self.cargo[1]
                        self.cargo = None
                    new_cargo = None
                    amount = 0
                    for product in self.venue.outputs:
                        if self.venue.outputs[product] > amount:
                            new_cargo = product
                            amount = self.venue.outputs[product]
                    if new_cargo:
                        self.cargo = (new_cargo, min(max_load,
                                                                    self.venue.outputs[new_cargo]))                       
                        self.venue.outputs[new_cargo] -= min(max_load,
                                                                                  self.venue.outputs[new_cargo])
                    self.venue = self.job
                    self.goal = self.venue.entrance
                    self.state = "Hauling"
                    self.next_state = "Working"
                    self.path = iter(self.find_path(world))
                    self.destination = next(self.path)
            elif self.rect.topleft == world.grid[self.destination].rect.topleft:
                try:
                    self.destination = next(self.path)    
                except StopIteration as e:
                    print "No next destination in PATH!"
                    print e
                    print self.destination
                    print self.venue
            else:
                self.travel(world) 
        
        elif self.state == "Travelling":
            if self.rect.topleft == world.grid[self.goal].rect.topleft:
                self.index = self.goal
                if self.next_state in ["Working", "Logging"]:
                    if self not in self.venue.workers:
                        self.venue.workers.append(self)
                    self.venue.en_route_workers.remove(self)
                else:
                    self.venue.patrons.append(self)
                    try:
                        self.venue.en_route_patrons.remove(self)
                    except ValueError as e:
                        print e
                        print "elf not in venue.patrons"
                        print "job: ", self.job.name
                        print "venue: ", self.venue.name
                        print "next state: ", self.next_state                        
                self.state = self.next_state
            elif self.rect.topleft == world.grid[self.destination].rect.topleft:
                try:
                    self.destination = next(self.path)    
                except StopIteration as e:
                    print e
                    print "no next destination in path"
                    print self.destination
                    print self.venue
                    
            else:
                self.travel(world)  


class Reindeer(object):
    velocities = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1),
                       (1, -1), (1, 0), (1, 1)]
    def __init__(self, center, speed, barn):
        self.name = random.choice(elfnames.REINDEER)
        self.velocity = random.choice(self.velocities)
        self.images = {(-1, -1): it.cycle([prepare.GFX["leftreindeer1"],
                                                         prepare.GFX["leftreindeer2"]]),
                              (-1, 0): it.cycle([prepare.GFX["leftreindeer1"],
                                                       prepare.GFX["leftreindeer2"]]),
                              (-1, 1): it.cycle([prepare.GFX["leftreindeer1"],
                                                       prepare.GFX["leftreindeer2"]]),
                              (0, -1): it.cycle([prepare.GFX["upreindeer"]]),
                              (0, 0): it.cycle([prepare.GFX["leftreindeer1"]]),
                              (0, 1): it.cycle([prepare.GFX["downreindeer"]]),
                              (1, -1): it.cycle([prepare.GFX["rightreindeer1"],
                                                       prepare.GFX["rightreindeer2"]]),
                              (1, 0): it.cycle([prepare.GFX["rightreindeer1"],
                                                      prepare.GFX["rightreindeer2"]]),
                              (1, 1): it.cycle([prepare.GFX["rightreindeer1"],
                                                      prepare.GFX["rightreindeer2"]])}
        self.image = next(self.images[self.velocity])
        self.rect = self.image.get_rect(center=center)
        self.speed = speed
        self.barn = barn
        
    def move(self, offset):
        self.rect.move_ip(offset)
        self.rect.clamp_ip(self.barn.deer_rect)
        
    def update(self, world):
        for worker in self.barn.workers:
            husbandry = worker.skills["Husbandry"]
            if self.barn.inputs["Moss"] >= .01:
                self.barn.outputs["Milk"] += .01 * husbandry
                self.barn.inputs["Moss"] -= .01
            if self.barn.inputs["Carrot"] >= .005:
                self.barn.inputs["Carrot"] -= .005
                if not random.randint(0, int(25000 * (1 - husbandry))) and len(self.barn.reindeers) < 10:
                    self.barn.reindeers.append(Reindeer(self.barn.rect.center,
                                                                          random.randint(1, 10),
                                                                          self.barn))               
        if not random.randint(0, 10):
            self.velocity = random.choice(self.velocities)
            self.image = next(self.images[self.velocity])
        if not world.ticks % 6:
            self.image = next(self.images[self.velocity])           
        self.move(self.velocity)
        
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)