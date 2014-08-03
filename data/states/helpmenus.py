import pygame as pg
from .. import tools, prepare
from ..components.labels import Label, GroupLabel, Button, PayloadButton, Menu

class MiddlemanMenu(tools._State):
    """Creates a menu to naviagte to other menus"""
    def __init__(self, next_state=None, menu_size=(400, 500),
                         title=None, title_space=20, title_lines=None,
                         title_line_left=15, title_line_space=20,
                         button_info=None, button_width=120,
                         button_height=50, button_spacer=20):
        super(MiddlemanMenu, self).__init__()
        self.next_state = next_state
        self.cursor = prepare.GFX["questionmark"]
        
        self.menu = Menu((menu_size))
        menu = self.menu.rect
        font = prepare.FONTS["weblysleekuil"]
        dark_font = prepare.FONTS["weblysleekuisl"] 
        done_label = Label(dark_font, 18, "DONE", "gray1", {"topleft": (0, 0)},
                                     "white")
        self.done_button = Button(menu.centerx - 40,
                                                menu.bottom - 60, 80, 50,
                                                done_label)
        
        
        self.labels = []
        top = menu.top + 5
        if title:
            title_label = GroupLabel(self.labels, font, 32, title, "darkgreen",
                                                {"midtop": (menu.centerx, top)})
            top += title_label.rect.height + title_space 
        if title_lines:
            for line in title_lines:
                label = GroupLabel(self.labels, font, 16, line, "gray1",
                                            {"topleft": (menu.left + title_line_left, top)})
                top += label.rect.height + 1                
            top += title_line_space
        self.buttons = []
        if button_info:
            for name, payload in button_info:
                label = Label(font, 24, name, "gray1", {"center": (0, 0)})
                button = PayloadButton(menu.centerx - button_width//2,
                                                    top, button_width, button_height,
                                                    label, payload)
                self.buttons.append(button)
                top += button.rect.height + button_spacer
    
    
    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.done_button.rect.collidepoint(event.pos):
                    self.next = self.next_state
                    self.done = True
                    return
                for button in self.buttons:
                    if button.rect.collidepoint(event.pos):
                        self.next = button.payload
                        self.done = True
                        break
                        
            elif event.button == 3:
                self.next = self.next_state
                self.persist["helping"] = False
                self.done = True
                
                
    def update(self, surface, keys, dt):
        self.draw(surface)
        
    def draw(self, surface):
        surface.fill(pg.Color("gray96"))
        self.persist["world"].draw(surface)
        self.menu.draw(surface)
        for label in self.labels:
            label.draw(surface)
        for button in self.buttons:
            button.draw(surface)
        self.done_button.draw(surface)
        surface.blit(self.cursor, pg.mouse.get_pos())
        
    
class HelpMenu(MiddlemanMenu):
    def __init__(self):
        button_info = [("Elves", "ELFHELP"),
                              ("Buildings", "BUILDINGTYPESELECTION"),
                              ("Items", "ITEMSHELP"),
                              ("Controls", "CONTROLSHELP")]  
        super(HelpMenu, self).__init__(next_state="MANAGING",
                                                      button_info=button_info)

    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.done_button.rect.collidepoint(event.pos):
                    self.next = self.next_state
                    self.persist["helping"] = False
                    self.done = True
                    return
                for button in self.buttons:
                    if button.rect.collidepoint(event.pos):
                        self.next = button.payload
                        self.done = True
                        break
                            
            elif event.button == 3:
                self.next = self.next_state
                self.persist["helping"] = False
                self.done = True
        
        
class ElfHelp(MiddlemanMenu):
    def __init__(self):
        lines = ["These industrious, fun-loving folk are the heart of your",
                    "operation. Meeting their needs and effectively utilizing",
                    "their unique abilities will be key to your success."]
        button_info = [("Needs", "NEEDSHELP"),
                              ("Qualities", "QUALITIESHELP"),
                              ("Skills", "SKILLSHELP")]  
        super(ElfHelp, self).__init__(next_state="HELPMENU",
                                                  title="Elves", title_lines=lines,
                                                  button_info=button_info)


class ItemsHelp(MiddlemanMenu):
    def __init__(self):
        lines = ["Items fall into three categories. Resources are the raw",
                    "materials harvested from the world. Goods are created",
                    "from resources and may be final products or materials",
                    "needed for toy production."]
        button_info = [("Resources", "RESOURCESHELP"),
                              ("Goods", "GOODSHELP"),
                              ("Toys", "TOYSHELP")]
        super(ItemsHelp, self).__init__(next_state="HELPMENU",
                                                       title="Items", title_lines=lines,
                                                       button_info=button_info)                      
