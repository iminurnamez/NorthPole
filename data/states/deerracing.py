import pygame as pg

from .. import tools, prepare
from ..components import racedeer 
from ..components import races
                           
                           
                           
                           
class DeerRacing(tools._State):
    def __init__(self):
        super(DeerRacing, self).__init__()
        self.next = "RACINGRESULTS"
        self.gallop_sound = prepare.SFX["gallop"] 
    
    def startup(self, persistant):
        self.race = races.Race(persistant["racers"], persistant["distance"],
                                         persistant["player"])
        self.player = persistant["player"]
        self.gallop_sound.play(-1)
        return tools._State.startup(self, persistant)
        
    def cleanup(self):
        self.persist["results"] = self.race.results 
        self.persist["player"] = self.player
        self.done = False
        return tools._State.cleanup(self)
    
    def update(self, surface, keys, dt):
        if self.race.done:
            self.gallop_sound.stop()
            self.done = True
        self.race.update()
        self.race.draw(surface)
    
    
