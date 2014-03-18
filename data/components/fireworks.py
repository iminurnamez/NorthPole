import itertools as it
from .. import prepare

class Firework(object):
    def __init__(self, center_point, x_velocity, y_velocity, altitude):
        self.start_y = center_point[0]
        self.rocket_images = it.cycle(prepare.GFX["rocket"])
        self.rocket_rect = self.rocket_image.get_rect(center=center_point)
        self.images = it.cycle([prepare.GFX["firework" + str(i) for i in range(1, 15)])
        self.altitude = altitude
        
        
    def display(self, surface):
        if not self.exploded:
            if not self.covered:        
                surface.blit(self.rocket_image, self.rocket_rect)
        else:
            surface.blit(self.image, self.rect)            
            
    def update(self, world):
        if not self.exploded:
            self.covered = False
            for item in [x for x in it.chain(world.trees, world.buildings,
                              world.decorations) if x.rect.bottom < self.start_y]:
                if item.rect.collidepoint(self.x_pos, self.y_pos):
                    self.covered = True
                    break
        
            if self.y_pos >= self.altitude:
                self.exploded = True
                self.image = next(self.images)
                self.rect = self.image.get_rect(center = self.rocket_rect.center)
                self.ticks = 1
            else:
                self.x_pos += self.x_velocity
                self.y_pos += self.y_velocity
                self.rocket_rect.center = (int(self.x_pos, int(self.y_pos))
        else:    
            try:
                if not self.ticks % 5:
                    self.image = next(self.images)
            except StopIteration:
                self.done = True
        self.ticks += 1
        