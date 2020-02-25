import pygame, random
hoehe = 800
breite = 800



def get_bushrects(level, playerrect):
    rects = []
    if level == 1:
        for i in range(20):
            a = pygame.Rect((random.randint(0, 1000), random.randint(0, 1000)), (30, 30))
            while playerrect.colliderect(a):
                a = pygame.Rect((random.randint(0, 1000), random.randint(0, 1000)), (30, 30))
            rects.append(a)
    return rects

def get_character(characternumber, walkorstand, hit = False):
    if characternumber == 1:
        character = 'Siegfried'
        hitwalkpic = [[pygame.image.load(f'Characters/{character}/hitstandfront.png'),
                    pygame.image.load(f'Characters/{character}/hitwalkfront1.png'),
                    # Hier werden die Bilder für die Animation des Spielers geladen
                    pygame.image.load(f'Characters/{character}/hitwalkfront2.png'),
                    pygame.image.load(f'Characters/{character}/hitstandfront.png')],
                   [pygame.image.load(f'Characters/{character}/hitstandback.png'),
                    pygame.image.load(f'Characters/{character}/hitwalkback1.png'),
                    pygame.image.load(f'Characters/{character}/hitwalkback2.png'),
                    pygame.image.load(f'Characters/{character}/hitstandback.png')],
                   [pygame.image.load(f'Characters/{character}/hitstandright.png'),
                    pygame.image.load(f'Characters/{character}/hitwalkright1.png'),
                    pygame.image.load(f'Characters/{character}/hitwalkright2.png'),
                    pygame.image.load(f'Characters/{character}/hitwalkright3.png')],
                   [pygame.image.load(f'Characters/{character}/hitstandleft.png'),
                    pygame.image.load(f'Characters/{character}/hitwalkleft1.png'),
                    pygame.image.load(f'Characters/{character}/hitwalkleft2.png'),
                    pygame.image.load(f'Characters/{character}/hitwalkleft3.png')]]
        hitstandpic = [pygame.image.load(f'Characters/{character}/hitstandfront.png'),
                    pygame.image.load(f'Characters/{character}/hitstandback.png'),
                    pygame.image.load(f'Characters/{character}/hitstandright.png'),
                    pygame.image.load(f'Characters/{character}/hitstandleft.png')]
        if hit and walkorstand == 'walk':
            return hitwalkpic
        elif hit and walkorstand != 'walk':
            return hitstandpic
    if characternumber == 2:
        character = 'Character1'
    if characternumber == 3:
        character = 'Ghost'
    walkpic = [[pygame.image.load(f'Characters/{character}/standfront.png'),
                pygame.image.load(f'Characters/{character}/walkfront1.png'),
                # Hier werden die Bilder für die Animation des Spielers geladen
                pygame.image.load(f'Characters/{character}/walkfront2.png'),
                pygame.image.load(f'Characters/{character}/standfront.png')],
               [pygame.image.load(f'Characters/{character}/standback.png'),
                pygame.image.load(f'Characters/{character}/walkback1.png'),
                pygame.image.load(f'Characters/{character}/walkback2.png'),
                pygame.image.load(f'Characters/{character}/standback.png')],
               [pygame.image.load(f'Characters/{character}/standright.png'),
                pygame.image.load(f'Characters/{character}/walkright1.png'),
                pygame.image.load(f'Characters/{character}/walkright2.png'),
                pygame.image.load(f'Characters/{character}/walkright3.png')],
               [pygame.image.load(f'Characters/{character}/standleft.png'),
                pygame.image.load(f'Characters/{character}/walkleft1.png'),
                pygame.image.load(f'Characters/{character}/walkleft2.png'),
                pygame.image.load(f'Characters/{character}/walkleft3.png')]]
    standpic = [pygame.image.load(f'Characters/{character}/standfront.png'),
                pygame.image.load(f'Characters/{character}/standback.png'),
                pygame.image.load(f'Characters/{character}/standright.png'),
                pygame.image.load(f'Characters/{character}/standleft.png')]
    if walkorstand == 'walk':
        return walkpic
    else:
        return standpic
def get_background(level):
    if level == 1:
        return 'bg.png'

def get_monster(level):
    pass