import pygame as pg
from .. import tools, prepare
from ..components.labels  import Label, GroupLabel as GLabel, Button, Menu


class InfoHelp(tools._State):
    def __init__(self, next_state=None, menu_size=(400, 700), title=None,
                        title_space=20, title_lines=None, info_pairs=None,
                        info_space=20):
        super(InfoHelp, self).__init__()
        self.next = next_state
        self.menu = Menu(menu_size)
        menu = self.menu.rect
        
        self.cursor = prepare.GFX["questionmark"]
        
        font = prepare.FONTS["weblysleekuil"]
        dark_font = prepare.FONTS["weblysleekuisl"]
        done_label = Label(font, 18, "DONE", "gray1", {"topleft": (0, 0)},
                                     "white")
        self.done_button = Button(menu.centerx - 40,
                                                menu.bottom - 60, 80, 50,
                                                done_label)
        self.labels = []
        title = GLabel(self.labels, font, 32, title, "darkgreen",
                             {"midtop": (menu.centerx, menu.top + 5)})
        
        
        
        top = title.rect.bottom + title_space

        lines = [] if title_lines is None else title_lines
        
        for line in lines:
            label = GLabel(self.labels, font, 14, line, "gray1",
                                  {"topleft": (menu.left + 20, top)})
            top += label.rect.height + 3
            
        info = [] if info_pairs is None else info_pairs         
                
                
        top += info_space
        for pair in info:
            name = GLabel(self.labels, dark_font, 18, pair[0], "gray1",
                                   {"topleft": (menu.left + 25, top)})
            top += 2
            for info_line in pair[1]:
                info_label = GLabel(self.labels, font, 14, info_line, "gray1",
                                             {"topleft": (menu.left + 160, top)})
                top += info_label.rect.height + 1
            top += 3 
            
    def get_event(self, event):
        if event.type  == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.done_button.rect.collidepoint(event.pos):
                    self.done = True
            elif event.button == 3:
                self.done = True
                
    def update(self, surface, keys, dt):
        self.draw(surface)
        
    def draw(self, surface):
        self.persist["world"].draw(surface)
        self.menu.draw(surface)
        for label in self.labels:
            label.draw(surface)
        self.done_button.draw(surface)
        surface.blit(self.cursor, pg.mouse.get_pos())
        

        
class SkillsHelp(InfoHelp):
    def __init__(self):
        lines = ["Each elf has a number of skills that influence how well they",
                    "perform different tasks. Skills slowly increase as elves use them.",
                    "Studying at a Schoolhouse will improve skills more quickly."]      
        info_pairs = [("Farming", ["Crops grow faster"]),
                            ("Logging", ["Harvest wood faster"]),
                            ("Mining", ["More productive mining"]),
                            ("Hauling", ["Haulers carry more per trip"]),
                            ("Husbandry", ["Better milk and wool collection",
                                                   "Animals more likely to breed"]),
                            ("Baking", ["More baked goods per batch"]), 
                            ("Woodworking", ["Millers are more productive",
                                                       "Woodwrights are more productive",
                                                       "and create higher quality toys"]),
                            ("Metalworking", ["Smelters are more productive",
                                                      "Metalsmiths are more productive",
                                                      "and create higher quality toys"]),
                            ("Stitchery", ["Spinsters are more productive",
                                                "Tailors are more productive", 
                                                "and create higher quality toys"]),
                            ("Dentistry", ["Faster dental procedures"])]
        super(SkillsHelp, self).__init__(next_state="ELFHELP", title="Skills", 
                                                      title_lines=lines, info_pairs=info_pairs)  

                                                      
class NeedsHelp(InfoHelp):
    def __init__(self):
        lines = ["Elves have certain basic needs which must be satisfied. Elves",
                    "will only go to their assigned job when all of their needs have",
                    "been met by visitng the appropriate type of building."]
        info_pairs = [("Energy", ["Elves will need to sleep in order to",
                                             "restore the energy they deplete",
                                             "while working."]),
                            ("Food", ["Providing adequate food is essential.",
                                          "Hungry elves will refuse to work."]),
                            ("Cheer", ["When the hectic monotony of work",
                                            "frazzles an elf's nerves, they will look",
                                            "for something fun to do"]),
                            ("Cavities", ["Elves' sugary diet makes them prone",
                                               "to tooth decay. If an elf's teeth become",
                                               "too cavity-riddled, they will need to",
                                               "visit a dentist."])]
        super(NeedsHelp, self).__init__(next_state="ELFHELP", title="Needs", 
                                                      title_lines=lines, info_pairs=info_pairs)
                                                      
                                                      
class QualitiesHelp(InfoHelp):
    def __init__(self):
        lines = ["Elves are born with innate, immutable qualities which", 
                    "affect their aptitude for certain activities."]
        info_pairs = [("Strength", ["Haulers can carry more per trip"]),
                            ("Wits", ["Elves learn faster at schoolhouses"]),
                            ("Mirth", ["Cheer decreases more slowly"]),
                            ("Charm", ["Entertainers are more effective",
                                             "Faster Husbandry skill acquisition"]),
                            ("Endurance", ["Slower energy depletion"]),
                            ("Mechanical", ["Easier to learn wood- and",
                                                   "metal-working"]),
                            ("Artistic", ["Stitchery and Baking are",
                                             "easier to learn"])]                            
        super(QualitiesHelp, self).__init__(next_state="ELFHELP", title="Qualities",
                                                           title_lines=lines, info_pairs=info_pairs)
        
        
        
class ResourcesHelp(InfoHelp):
    def __init__(self):
        info_pairs = [("Moss", ["Moss is the bulk of a reindeer's diet"]),
                            
                            ("Beet", ["Beets are converted into sugar at",
                                          "a refinery"]),
                            ("Carrot", ["Used by bakeries and carrot stands",
                                            "Carrots also make sheep and reindeer",
                                            "mating possible"]),
                            ("Colorberry", ["Colorberries are used for dyeing cloth", 
                                                  "and painting"]),
                            ("Ore", ["A mines can be built on an ore deposit",
                                        "Ore is refined into metal at a smeltery"]),
                            ("Reindeer", ["Reindeer produce milk if they have moss",
                                                "to eat and can be sold for cash"]),
                            ("Sheep", ["Wool will only grow back if the sheep",
                                            "has shrubbery to eat",
                                            "Sheep may be sold for cash"]),
                            ("Shrubbery", ["Sheep love the leafy foliage",
                                                  "from colorberry bushes"]),
                            ("Stone", ["Stone from a mine is needed to",
                                            "construct certain buildings"]),
                            ("Wood", ["Wood is harvested from trees and",
                                           "sent to a sawmill for processing"]),
                            ("Wool", ["Wool is sent to a Woollen Mill to",
                                          "be turned into cloth"])]
        super(ResourcesHelp, self).__init__(next_state="ITEMSHELP", title="Resources",
                                                             info_pairs=info_pairs, title_space=10,
                                                             info_space=0)        
                            
                            
class GoodsHelp(InfoHelp):
    def __init__(self):
        info_pairs = [("Carrot Cake", ["Made from carrots and sugar",
                                                    "Carrot cake is better for elves' teeth",
                                                    "but less satisfying than cookies"]),
                            ("Cloth", ["Produced from wool at a Woollen mill"]),
                            ("Cookies", ["Cookies are elves' favorite food",
                                              "Made from sugar at a bakery"]),
                            ("Lumber", ["Sawmills turn wood into lumber",
                                              "Lumber is needed to construct most",
                                              "buildings and for toy production"]),  
                            ("Metal", ["Metal from a smeltery can be",
                                           "fashioned into toys at a metalshop"]),
                            ("Milk", ["Reindeers can be milked if they have",
                                         "moss to eat"]),  
                            ("Sugar", ["Sugar is needed for baking"])]
                          
        super(GoodsHelp, self).__init__(next_state="ITEMSHELP", title="Goods",
                                                             info_pairs=info_pairs, title_space=10,
                                                             info_space=10)        

class ToysHelp(InfoHelp):
    def __init__(self):
        info_pairs = [("Hoop and Stick", [""]),
                            ("Firetruck", [""]),
                            ("Train Set", [""]),
                            ("Dollhouse", [""]),
                            ("Teddy Bear", [""]),
                            ("Doll", [""]),
                            ("Doll Clothes", [""]),
                            ("Checkers", [""]),
                            ("Paddleball", [""]),
                            ("Pop Gun", [""]),
                            ("Flute", [""]),
                            ("Bow and Arrow", [""]),
                            ("Baseball Bat", [""]),
                            ("Spring Toy", [""]),
                            ("Jack-in-the-Box", [""]),
                            ("Harmonica", [""]),
                            ("Kazoo", [""]),
                            ("Bell", [""]),
                            ("Socks", [""]),
                            ("", [""]),
                            ("", [""]),
                            ("", [""]),
                            ("", [""]),
                            ("", [""]),
                            ("", [""]),
                            ("", [""]),
                            ("", [""])]
        super(ToysHelp, self).__init__(next_state="ITEMSHELP", title="Toys",
                                                     info_pairs=info_pairs, title_space=10,
                                                     info_space=0)


class ControlsHelp(InfoHelp):
    def __init__(self):
        info_pairs = [("View Elf Info", "Click on elf"),
                            ("View Building Info", "Click on building"),
                            ("Change Speed", "Click + / - icons"),
                            ("Toggle Fullscreen", "Press F"),
                            ("Exit", "Close Window / ESCAPE")]
                                    
        super(ControlsHelp, self).__init__(next_state="HELPMENU", title="Controls",
                                                          info_pairs=info_pairs)
        
                                                          
#                                                          
 
 
 
 
 