


class BuildingTypeSelection(tools._State):
    def __init__(self):
        super(BuildingSelection, self).__init__()
        self.current = "All"
        self.building_type = None
        self.popup = pg.Rect(400, 500)
        title_label = Label(24, "Select a building type", "darkgreen", "center",
                                    0, 0, "white")
        back_label = Label(24, "BACK", "darkgreen", "center", 0, 0, "white")
        b_width = 120
        b_height = 80
        self.back_button = Button(self.popup.centerx - b_width/2,
                                                self.popup.bottom - (20 + b_height),
                                                b_width, b_height, back_label)
        types = ["Rest", "Merrymaking", "Feasting", "
    def display(self, surface):
        pg.draw.rect
    
    def update(self, surface, keys):
        if self.current = 
    
    def get_event(self, event):
        if event.type == pg.QUIT:
            self.next = "MANAGING"
            self.done = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            if self.back_button.rect.collidepoint(event.pos):
                self.next = "MANAGING"
                self.done = True
                