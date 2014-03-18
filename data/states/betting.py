

#---  0---|--- 10---|--- 20---|--- 30---|--- 40---|--- 50---|--- 60---|--- 70---|

from collections import OrderedDict
import random
import pygame as pg

from .. import tools
from ..components import racedeer
from ..components import elfnames
from ..components import wagers
from ..components.labels import TransparentLabel as TLabel
from ..components.labels import GroupLabel as GLabel
from ..components.labels import Label, Button, PayloadButton

class Betting(tools._State):
    #mods = [(1.7, (1, 9)), (1.8, (1, 5)), (1.9, (2, 5)), (2.0, (1, 2)),
    #              (2.1, (3, 5)), (2.2, (4, 5)), (2.3, (1, 1)), (2.4, (6, 5)),
    #              (2.5, (7, 5)), (2.6, (3, 2)), (2.7, (8, 5)), (2.8, (9, 5)),
    #              (2.9, (2, 1)), (3.0, (5, 2)), (3.1, (3, 1)), (3.2, (7, 2)),
    #              (3.3, (4, 1)), (3.4, (9, 2)), (3.5, (5, 1)), (3.6, (11, 2)),
    #              (3.7, (6, 1)), (3.8, (13, 2)), (3.9, (7, 1)), (4.0, (15, 2)),
    #              (4.1, (8, 1)), (4.2, (17, 2)), (4.3, (9, 1)), (100, (10, 1))]
    
    mods = [(1.5, (1, 9)), (1.6, (1, 5)), (1.7, (2, 5)), (1.8, (1, 2)),
                  (1.9, (3, 5)), (2.0, (4, 5)), (2.1, (1, 1)), (2.2, (6, 5)),
                  (2.3, (7, 5)), (2.4, (3, 2)), (2.5, (8, 5)), (2.6, (9, 5)),
                  (2.7, (2, 1)), (2.8, (5, 2)), (2.9, (3, 1)), (3.0, (7, 2)),
                  (3.1, (4, 1)), (3.2, (9, 2)), (3.3, (5, 1)), (3.4, (11, 2)),
                  (3.5, (6, 1)), (3.6, (13, 2)), (3.7, (7, 1)), (3.8, (15, 2)),
                  (3.9, (8, 1)), (4.0, (17, 2)), (4.1, (9, 1)), (100, (10, 1))]
    
    
    odds_dict = OrderedDict(mods)
    distance_map ={6000: "Sprint",
                              10000: "Mid-Distance",
                              16000: "Marathon"}
        
    def __init__(self):
        super(Betting, self).__init__()
        self.next = "DEERRACING"
        screen_rect = pg.display.get_surface().get_rect()
        colors = ["blue", "cyan", "red", "green2", "chartreuse",
                      "darkviolet", "deeppink", "yellow"]
        random.shuffle(colors)
        colors = iter(colors)
        names = iter(random.sample(elfnames.RACE, 8))
        self.racers = []
        for i in range(1, 9):
            name = next(names)
            color = next(colors)
            speed = random.randint(50, 99)
            stamina = random.randint(50, 99)
            self.racers.append(racedeer.RaceDeer((0, (i - 1) * 50), name, i,
                                                                     color, speed, stamina))
        distances = [6000.0, 10000.0, 16000.0]
        self.distance = random.choice(distances)
        tot_score = sum([x.speed + (
                                   x.stamina / (18000.0 / self.distance)) for 
                                   x in self.racers])
        avg_score = tot_score / len(self.racers)
        
        self.labels = []
        self.title = GLabel(self.labels, 32, "Mistletoe Downs", "darkgreen",
        "midtop",
                                          screen_rect.left + 200, 10, "white")
        self.race_title = GLabel(self.labels, 24,
                                           self.distance_map[self.distance],
                                           "gray1", "midtop", self.title.rect.centerx, 
                                           self.title.rect.bottom + 10, "white") 
        self.header1 = GLabel(self.labels, 18, "# Name", "darkgreen",
                                         "topleft", 35, self.title.rect.bottom + 50, "white")
        self.header2 = GLabel(self.labels, 18, "Odds", "darkgreen", "topleft",
                                         210, self.title.rect.bottom + 50, "white")
        self.header3 = GLabel(self.labels, 18, "Speed   Stamina", "darkgreen",
                                                "topleft", 280, self.title.rect.bottom + 50,
                                                "white")
        self.screen_rect = screen_rect
        self.right_rect = pg.Rect(450, 0, screen_rect.width - 450,
                                             screen_rect.height - 300)
        self.bottom_rect = pg.Rect(0, self.right_rect.bottom - 1,
                                                 screen_rect.width,
                                                 screen_rect.height - 
                                                 self.right_rect.bottom)
        self.middle_rect = pg.Rect(700, self.right_rect.bottom,
                                                screen_rect.width - 700, 
                                                screen_rect.height - 
                                                self.right_rect.bottom) 
        top = self.header1.rect.bottom + 20
        for racer in self.racers:
            score = (racer.speed + 
                         (racer.stamina / (18000.0 / self.distance)))
            racer.score = (avg_score /  (3 * float(score))) * (tot_score/
                                                                                   (float(score)))
            for key in self.odds_dict:
                if racer.score < key:
                    racer.odds_text = "{}:{}".format(self.odds_dict[key][0],
                                                                      self.odds_dict[key][1])
                    racer.odds = (float(self.odds_dict[key][0]) / 
                                               self.odds_dict[key][1])
                    break
            
            racer.name_label = TLabel(16, "{0:5})  {1}".format(racer.num,
                                                    racer.name), "gray1", "topleft", 5,
                                                    top, "white")
            racer.odds_label =  Label(16, racer.odds_text, "gray1", "topleft",
                                                  230, top, "white")           
            racer.stats_label = Label(16, "{}{:18}".format(racer.speed,
                                                 racer.stamina), "gray1", "topleft", 310,
                                                 top, "white")
            top += 40
        
        
        new_top = self.bottom_rect.top + 15
        
        self.wager_types = ["Win", "Place", "Show", "Quinella", "Exacta",
                                      "Trifecta"]
        self.current_wager = ""
        self.current_amount = 0
        self.current_deers = []
        
        self.wager_buttons = []
        self.cur_title = GLabel(self.labels, 18, "Bet Type: ", "gray1", 
                                    "topleft", 20, new_top + 10, "white")
        
        horiz = 250
        
        for wt in self.wager_types:
            wt_label = TLabel(12, wt, "gray1", "topleft", 0, 0, "lightgray")
            button = PayloadButton(horiz, new_top, 60, 40, wt_label, wt)
            self.wager_buttons.append(button)
            horiz += 70
        new_top += button.rect.height + 20
        self.amt_title = GLabel(self.labels, 18, "Bet Amount: ", "gray1",
                                     "topleft", 20, new_top + 20, "white")
        self.amount_buttons = []
        horiz = 250
        for num in [1, 5, 10, 25, 100, 500, 1000]:
            pos_label = TLabel(12, "+{}".format(num), "gray1", "topleft",
                                         0, 0, "lightgray")
            pos_button = PayloadButton(horiz, new_top, 50, 30, pos_label,
                                                       num)
            neg_label = TLabel(12, "-{}".format(num), "gray1", "topleft",
                                         0, 0, "lightgray")
            neg_button = PayloadButton(horiz, new_top + 40, 50, 30,
                                                       neg_label, -num)                               
            self.amount_buttons.append(pos_button)
            self.amount_buttons.append(neg_button)
            horiz += 60
        new_top += 90    
        self.picks_title = GLabel(self.labels, 18, "Picks: ", "gray1",
                                     "topleft", 20, new_top + 20, "white")
        horiz = 250
        self.pick_buttons = []
        i = 0
        for reindeer in self.racers:
            p_label = TLabel(16, "{}".format(reindeer.num), "gray1",
                                      "topleft", 0, 0, "lightgray")
            p_button = PayloadButton(horiz, new_top, 50, 30, p_label,
                                                    reindeer)
            self.pick_buttons.append(p_button)
            horiz += 60
            i += 1
            if i == 4:
                horiz = 250
                new_top += 40
                
        r_label = TLabel(14, "Remove", "gray1", "topleft", 0, 0, "lightgray")
        self.remove_button = Button(horiz, new_top, 70, 30, r_label)
        place_label = TLabel(18, "Place Bet", "gray1", "topleft", 0, 0,
                                       "lightgray")
        self.place_button = Button(50, self.screen_rect.bottom - 60, 120, 50,
                                                place_label)
        start_label = TLabel(48, "Start Race", "gray1", "topleft", 0, 0,
                                      "lightgray")
        self.start_button = Button(self.middle_rect.centerx - 125,
        self.screen_rect.bottom - 140, 250, 120, start_label)
        self.cash_title = GLabel(self.labels, 24, "Cash: ", "gray1", "topleft", 
                                            self.middle_rect.left + 10,
                                            self.middle_rect.top + 10, "white")
        self.total_title = GLabel(self.labels, 24, "Total Wagers: ", "gray1",
                                           "topleft", self.cash_title.rect.left, 
                                           self.cash_title.rect.bottom + 10, "white")
        
        self.bet_map = {"Win": wagers.WinWager,
                                 "Place": wagers.PlaceWager,
                                 "Show": wagers.ShowWager,
                                 "Quinella": wagers.QuinellaWager,
                                 "Exacta": wagers.ExactaWager,
                                 "Trifecta": wagers.TrifectaWager}

    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            for button in self.wager_buttons:
                if button.rect.collidepoint(event.pos):
                    self.current_wager = button.payload
            for amt_button in self.amount_buttons:
                if amt_button.rect.collidepoint(event.pos):
                    if amt_button.payload + self.current_amount < 0:
                        pass
                    elif (self.player.cash - (amt_button.payload +
                                                      self.current_amount) < 0):
                        pass
                    else:
                        self.current_amount += amt_button.payload
                        
            for pick_button in self.pick_buttons:
                if pick_button.rect.collidepoint(event.pos):
                    self.current_deers.append(pick_button.payload)
            if self.remove_button.rect.collidepoint(event.pos):
                if self.current_deers:
                    self.current_deers.pop()
            if self.place_button.rect.collidepoint(event.pos):
                bet_nums = {"Win": 1,
                                     "Place": 1,
                                     "Show": 1,
                                     "Quinella": 2,
                                     "Exacta": 2,
                                     "Trifecta": 3}
                if (self.current_wager and
                     len(self.current_deers) == bet_nums[self.current_wager]):
                    self.player.bets.append(self.bet_map[self.current_wager](
                                                                    self.current_deers,
                                                                    self.current_amount))
                    self.player.cash -= self.current_amount
                    self.current_amount = 0
                    self.current_wager = ""
                    self.current_deers = []
            if self.start_button.rect.collidepoint(event.pos):
                self.done = True

    def update(self, surface, keys):
        self.dynamics = []
        
        self.bet_type_label = GLabel(self.dynamics, 14,
                                                   "{}".format(self.current_wager), "gray1",
                                                   "midleft", self.cur_title.rect.right + 5,
                                                   self.cur_title.rect.centery, "white")
        self.amount_label = GLabel(self.dynamics, 14,
                                                 "${:.2f}".format(self.current_amount),
                                                 "gray1", "midleft",
                                                 self.amt_title.rect.right + 5,
                                                 self.amt_title.rect.centery, "white")
        self.picks_label = GLabel(self.dynamics, 14, "{}".format("-".join(
                                             [str(x.num) for x in self.current_deers])), 
                                             "gray1", "midleft", 
                                             self.picks_title.rect.right + 5, 
                                             self.picks_title.rect.centery, "white")
        left = 500
        top = 50
        for player_bet in self.player.bets:
            pb_label = GLabel(self.dynamics, 16, player_bet.text, "gray1",
                                        "topleft", left, top, "white")
            top += 20
        cash_label = GLabel(self.dynamics, 16, "${:.2f}".format(self.player.cash), "gray1",
                                       "bottomleft", self.cash_title.rect.right + 2, 
                                       self.cash_title.rect.bottom - 1, "white") 
        
        total_bets = sum([x.amount for x in self.player.bets])
        bets_label = GLabel(self.dynamics, 16, "${:.2f}".format(total_bets), "gray1",
                                       "bottomleft", self.total_title.rect.right + 2, 
                                       self.total_title.rect.bottom - 1, "white") 
        
        
        surface.fill(pg.Color("white"))
        pg.draw.rect(surface, pg.Color("gray10"), self.screen_rect, 5)
        pg.draw.rect(surface, pg.Color("gray10"), self.right_rect, 5) 
        pg.draw.rect(surface, pg.Color("gray10"), self.bottom_rect, 5)
        pg.draw.rect(surface, pg.Color("gray10"), self.middle_rect, 5)
        for label in self.labels:
            label.display(surface)
        for button in self.wager_buttons:
            button.display(surface)
        for a_button in self.amount_buttons:
            a_button.display(surface)
        for p_button in self.pick_buttons:
            p_button.display(surface)
        self.remove_button.display(surface)
        self.place_button.display(surface)
        self.start_button.display(surface)
        for d_label in self.dynamics:
            d_label.display(surface)
        for racer in self.racers:
            racer.name_label.display(surface)
            racer.odds_label.display(surface)
            racer.stats_label.display(surface)

    def startup(self, persistant):
        self.__init__()
        self.player = persistant["player"]
        return tools._State.startup(self, persistant)    

    def cleanup(self):
        self.persist["racers"] = self.racers
        self.persist["distance"] = self.distance
        self.persist["player"] = self.player
        self.done = False
        return self.persist