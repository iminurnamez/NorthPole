import pygame as pg
from .. import tools, prepare
from ..components.labels  import Label, GroupLabel as GLabel, Button, Menu


class SkillsHelp(tools._State):
    def __init__(self):
        super(SkillsHelp, self).__init__()
        self.next = "ELFHELP"
        self.menu = Menu((400, 700))
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
        title = GLabel(self.labels, font, 32, "Skills", "darkgreen",
                             {"midtop": (menu.centerx, menu.top + 5)})
        
        
        
        top = title.rect.bottom + 10

        lines = ["Each elf has a number of skills that influence how well they",
                    "perform different tasks. Skills slowly increase as elves use them.",
                    "Studying at a Schoolhouse will improve skills more quickly."]      
        for skill_line in lines:
            skill_label = GLabel(self.labels, font, 14, skill_line, "gray1", {"topleft": (menu.left + 20, top)})
            top += skill_label.rect.height + 3
            
        skill_info = [         
                ("Farming", ("Crops grow faster",)),
                ("Logging", ("Harvest wood faster",)),
                ("Mining", ("More productive mining",)),
                ("Hauling", ("Haulers carry more per trip",)),
                ("Husbandry", ("Better milk and wool collection",
                                       "Animals more likely to breed")),
                ("Baking", ("More baked goods per batch",)), 
                ("Woodworking", ("Millers are more productive",
                                           "Woodwrights are more productive",
                                           "and create higher quality toys")),
                ("Metalworking", ("Smelters are more productive",
                                           "Metalsmiths are more productive",
                                           "and create higher quality toys")),
                ("Stitchery", ("Spinsters are more productive",
                                    "Tailors are more productive", 
                                    "and create higher quality toys")),
                ("Dentistry", ("Faster dental procedures",))]
                
        top += 5
        for skill in skill_info:
            name = GLabel(self.labels, dark_font, 18, skill[0], "gray1", {"topleft": (menu.left + 15, top)})
            top += 2
            for info in skill[1]:
                info = GLabel(self.labels, font, 14, info, "gray1", {"topleft": (menu.left + 160, top)})
                top += info.rect.height + 1
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
        