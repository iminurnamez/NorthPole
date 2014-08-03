import pygame as pg
from .. import tools, prepare
from ..components.labels import GroupLabel as GLabel, Label, Button

class RaceResults(tools._State):    
    def __init__(self):
        super(RaceResults, self).__init__()
        self.cursor = prepare.GFX["canecursor"]
        self.next = "MANAGING"
        self.font = prepare.FONTS["weblysleekuil"]
        
    def setup(self, results):    
        self.results = results
        screen_rect = pg.display.get_surface().get_rect()
        self.labels = []
        y_pos = 10
        title = GLabel(self.labels, self.font, 24, "Race Results", "gray1", 
                             {"midtop": (screen_rect.centerx, y_pos)}, "white")
        y_pos += title.rect.height + 20
        for result in self.results:
            result.name_label.rect.topleft = (50, y_pos)
            y_pos += result.name_label.rect.height + 5
        y_pos += 10
        bet_title = GLabel(self.labels, self.font, 18, "Winning Bets", "gray1",
                                    {"midtop": (screen_rect.centerx, y_pos)}, "white")
        y_pos += 30
        for bet in self.player.bets:
            if bet.is_a_winner(results):
                bet_label = GLabel(self.labels, self.font, 16, bet.text, "gray1",
                                             {"center": (screen_rect.centerx, y_pos)},
                                             "white")
                payout_label = GLabel(self.labels, self.font, 16, 
                                                  "Payout: ${:.2f}".format(bet.payout),
                                                  "gray1", 
                                                  {"midtop": (screen_rect.centerx, 
                                                  bet_label.rect.bottom + 5)}, "white")
                self.player.cash += bet.payout
                y_pos += 60
        self.player.bets = []
        button_width = 120
        button_height = 90
        new_label = Label(self.font, 24, "NEW RACE", "darkgreen", {"center": (0, 0)}, "white")
        self.new_button = Button(screen_rect.centerx - button_width/2,
                                         screen_rect.bottom - (30 + (button_height * 2)),
                                         button_width, button_height, new_label)
        quit_label = Label(self.font, 24, "QUIT", "darkgreen", {"center": (0, 0)}, "white")
        self.quit_button = Button(screen_rect.centerx - button_width/2,
                                         screen_rect.bottom - (10 + button_height),
                                         button_width, button_height, quit_label)
        
    def startup(self, persistant):
        self.player = persistant["player"] 
        self.setup(persistant["results"])
        return tools._State.startup(self, persistant)
        
    def cleanup(self):
        self.persist["player"] = self.player
        self.done = False
        return tools._State.cleanup(self)
    
    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.new_button.rect.collidepoint(event.pos):
                self.next = "BETTING"
                self.done = True
            elif self.quit_button.rect.collidepoint(event.pos):
                self.next = "MANAGING"
                self.done = True
                
    def update(self, surface, keys, dt):
        surface.fill(pg.Color("white"))
        for result in self.results:
            result.name_label.draw(surface)
        for label in self.labels:
            label.draw(surface)
        self.new_button.draw(surface)
        self.quit_button.draw(surface)
        surface.blit(self.cursor, pg.mouse.get_pos())        
        
        
        