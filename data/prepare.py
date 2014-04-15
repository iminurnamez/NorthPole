import os
import pygame as pg

from . import tools
from .components import players
SCREEN_SIZE = (1080, 740)
ORIGINAL_CAPTION = "North Pole Tycoon: Old-Timey Toys Division"


#Initialization
pg.init()
os.environ['SDL_VIDEO_CENTERED'] = "TRUE"
pg.display.set_caption(ORIGINAL_CAPTION)
SCREEN = pg.display.set_mode(SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()

#Resource loading (Fonts and music just contain path names).
FONTS = tools.load_all_fonts(os.path.join("resources", "fonts"))
MUSIC = tools.load_all_music(os.path.join("resources", "music"))
SFX   = tools.load_all_sfx(os.path.join("resources", "sound"))
GFX   = tools.load_all_gfx(os.path.join("resources", "graphics"))
pics = [GFX["firework" + str(i)] for i in range(1, 15)]
pics2 = [GFX["firework_ring" + str(i)] for i in range(1, 15)]
for index, pic in enumerate(pics, 1):
   for color in ["mediumorchid3", "dodgerblue4", "orangered", "green2", "red3", "darkorchid",
                      "aquamarine3", "maroon1", "lightseagreen", "darkgreen", "red4", "red2", "forestgreen", "green", "blue", "cyan",
                      "slategray1",
                  "darkgoldenrod",]:
        surf = pg.Surface(pic.get_rect().size).convert()
        surf.set_colorkey((0,0,0, 255))
        pg.transform.threshold(surf, pic, (0,0,0,255), (0,0,0,0), pg.Color(color))
        GFX[color + "firework" + str(index)] = surf
for index, pic in enumerate(pics2, 1):
    for color in ["dodgerblue4", "orangered", "green2", "red3", "darkorchid", "cyan", "slategray1",
                  "darkgoldenrod", "aquamarine3", "maroon1", "lightseagreen", "darkgreen", "mediumorchid3", "green", "blue",  "red4", "red2", "forestgreen"]:
         surf = pg.Surface(pic.get_rect().size).convert()
         surf.set_colorkey((0,0,0, 255))
         pg.transform.threshold(surf, pic, (0,0,0,255), (0,0,0,0), pg.Color(color))
         GFX[color + "firework_ring" + str(index)] = surf
     

PLAYER = players.Player()
