import pygame as pg
from .. import tools
from ..components.labels import GroupLabel as GLabel

class RaceResults(tools._State):    
    def __init__(self):
        super(RaceResults, self).__init__()
        self.next = "MANAGING"
        
        
    def setup(self, results):    
        self.results = results
        screen_rect = pg.display.get_surface().get_rect()
        self.labels = []
        y_pos = 10
        title = GLabel(self.labels, 24, "Race Results", "gray1", "midtop", 
                             screen_rect.centerx, y_pos, "white")
        y_pos += title.rect.height + 20
        for result in self.results:
            result.name_label.rect.topleft = (50, y_pos)
            y_pos += result.name_label.rect.height + 5
        y_pos += 10
        bet_title = GLabel(self.labels, 18, "Winning Bets", "gray1",
                                    "midtop", screen_rect.centerx, y_pos, "white")
        y_pos += 30
        for bet in self.player.bets:
            if bet.is_a_winner(results):
                bet_label = GLabel(self.labels, 16, bet.text, "gray1",
                                             "center", screen_rect.centerx, y_pos,
                                             "white")
                payout_label = GLabel(self.labels, 16, 
                                                  "Payout: ${:.2f}".format(bet.payout),
                                                  "gray1", "midtop", 
                                                  screen_rect.centerx, 
                                                  bet_label.rect.bottom + 5, "white")
                self.player.cash += bet.payout
                y_pos += 60
        self.player.bets = []
        
    def startup(self, persistant):
        self.player = persistant["player"] 
        print persistant["results"]
        self.setup(persistant["results"])
        return tools._State.startup(self, persistant)
        
    def cleanup(self):
        self.persist["player"] = self.player
        self.done = False
        return tools._State.cleanup(self)
    
    def get_event(self, event):
        if (event.type == pg.KEYDOWN or 
                        event.type == pg.MOUSEBUTTONDOWN):
            self.done = True

    def update(self, surface, keys):
        surface.fill(pg.Color("white"))
        for result in self.results:
            result.name_label.display(surface)
        for label in self.labels:
            label.display(surface)        
        
        
        