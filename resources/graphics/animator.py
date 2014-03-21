import sys
import itertools as it
import pygame as pg

       
def main(fps, image_paths, bg_color="black"):
    pg.init()
    screen = pg.display.set_mode((640, 480))
    clock = pg.time.Clock()
    
    images = it.cycle([pg.image.load(x).convert() for x in image_paths])
    image = next(images)
    test_rect = image.get_rect(center=(320, 240))
    animation_rate = 5
    
    ticks = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    animation_rate += 1
                    print animation_rate
                elif event.key == pg.K_DOWN and animation_rate > 1:
                    animation_rate -= 1

        if not ticks % animation_rate:
            image = next(images)        
                
        screen.fill(pg.Color(bg_color))
        screen.blit(image, test_rect)
        pg.display.update()
        clock.tick(fps)
        ticks += 1

        
main(60, ["wavy1.png", "wavy2.png"])       
#main(40, ["firework_ring" + str(x) + ".png" for x in range(1, 15)])        
#main(30, ["racedeer1.png", "racedeer1.png", "racedeer1.png", "racedeer1.png", "racedeer1.png", "racedeer2.png", "racedeer3.png", "racedeer2.png"])
#main(60, ["chop3.png", "chop1.png", "chop2.png", "chop1.png", "chop3.png"])
#main(60, ["candywindow" + str(x) + ".png" for x in range(1, 10)])
#main(40, ["skaterleft1.png", "skaterleft2.png", "skaterleft3.png", "skaterleft2.png", "skaterleft1.png"]) 
#main(40, ["elfleftskate1.png", "elfleftskate2.png", "elfleftskate2.png", "elfleftskate3.png", "elfleftskate2.png", "elfleftskate2.png"])
#main(30, ["puppet1.png", "puppet2.png", "puppet3.png", "puppet4.png", "puppet5.png", "puppet6.png", "puppet7.png",
#               "puppet8.png", "puppet9.png", "puppet10.png", "puppet11.png", "puppet12.png", "puppet13.png", "puppet14.png",
#               "puppet15.png", "puppet16.png", "puppet17.png"])