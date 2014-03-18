class Wager(object):                
    def __init__(self, bet_type, racers, amount):
        self.bet_type = bet_type
        self.racers = racers
        self.amount = amount
        self.text = "${:.2f}   {:10}   {}".format(self.amount, self.bet_type,
                                                                self.racers[0].num)
    
class WinWager(Wager):
    def __init__(self, racers, amount):
        super(WinWager, self).__init__("Win", racers, amount)
        self.payout = amount + (amount * self.racers[0].odds)
        
    def is_a_winner(self, results):
        return self.racers[0] == results[0]
           
        
class PlaceWager(Wager):
    def __init__(self, racers, amount):
        super(PlaceWager, self).__init__("Place", racers, amount)
        self.payout = amount + (amount * (self.racers[0].odds * .54))
        
    def is_a_winner(self, results):
        return self.racers[0] in results[:2]    

class ShowWager(Wager):
    def __init__(self, racers, amount):
        super(ShowWager, self).__init__("Show", racers, amount)
        self.payout = amount + (amount * (self.racers[0].odds * .31))
    def is_a_winner(self, results):
        return self.racers[0] in results[:3]
        
class QuinellaWager(Wager):
    def __init__(self, racers, amount):
        super(QuinellaWager, self).__init__("Quinella", racers, amount)
        self.payout = amount + (sum([x.odds * .54 for x in self.racers]) * 
                                                     1.7 * amount)
        self.text = "${:.2f}   {:10}  {}-{}".format(self.amount, self.bet_type, 
                                                                     self.racers[0].num,
                                                                     self.racers[1].num)
        
    def is_a_winner(self, results):
        top_two = results[:2]
        return self.racers[0] in top_two and self.racers[1] in top_two 
            
class ExactaWager(Wager):
    def __init__(self, racers, amount):
        super(ExactaWager, self).__init__("Exacta", racers, amount)
        self.payout = amount + (sum([x.odds * .54 for x in self.racers]) * 
                                                     2.4 * amount)
        self.text = "${:.2f}   {:10}  {}-{}".format(self.amount, self.bet_type,
                                                                     self.racers[0].num, 
                                                                     self.racers[1].num)
    
    def is_a_winner(self, results):
        return self.racers[0] == results[0] and self.racers[1] == results[1]
        
        
    
class TrifectaWager(Wager):
    def __init__(self, racers, amount):
        super(TrifectaWager, self).__init__("Trifecta", racers, amount)
        self.payout = amount + (amount * 
                                             sum([x.odds * .45 for x in self.racers]) * 9.7)
        self.text = "${:.2f}  {:10}  {}-{}-{}".format(self.amount, self.bet_type,
                                                                          self.racers[0].num,
                                                                          self.racers[1].num,
                                                                          self.racers[2].num)
        
    def is_a_winner(self, results):
        return (self.racers[0] == results[0] and
                    self.racers[1] == results[1] and
                    self.racers[2] == results[2])
            