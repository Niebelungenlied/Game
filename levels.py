import pygame, random
hoehe = 800
breite = 800



def get_bushrects(level):
    rects = []
    if level == 1:
        for i in range(20):
            rects.append(pygame.Rect((random.randint(0, 1000), random.randint(0, 1000)), (30, 30)))
    return rects

def get_character(characternumber):
    if characternumber == 1:
        return 'Character1'

def get_background(level):
    if level == 1:
        return 'bg.png'
