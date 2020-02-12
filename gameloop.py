import pygame
import time

walkpic = standpic = []


def loadcharacter(charnumb):
    global walkpic
    global standpic
    character = 'Character1'  # Hier soll ein Charakter ausgesucht werden
    walkpic = [[pygame.image.load(f'Characters/{character}/standfront.png'),
                pygame.image.load(f'Characters/{character}/walkfront1.png'),   # Hier werden die Bilder für die Animation des Spielers geladen
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


class Player:
    def __init__(self, size, display, startpos):
        loadcharacter(1)
        self.size = size
        self.display = display
        self.rectplayer = pygame.Rect(0,0, size, size)
        self.rectplayer.center = startpos
        self.levelrect = pygame.Rect(0, 0, 500, 500)
        self.starttime = time.time()
        self.nextframe = 80
        self.frame = 0
        self.direction = 0
        self.speeed = 1

    def move(self):  # Hier wird der Spieler bewegt
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            if self.levelrect.contains(self.rectplayer.move(0, -1)):
                self.rectplayer = self.rectplayer.move(0, -1)
                self.is_walking = True
                self.direction = 1
        else:
            self.is_walking = False
        if keys[pygame.K_DOWN]:
            if self.levelrect.contains(self.rectplayer.move(0, 1)):
                self.rectplayer = self.rectplayer.move(0, 1)
                self.is_walking = True
                self.direction = 0
            else:
                self.is_walking = False
        if keys[pygame.K_RIGHT]:
            if self.levelrect.contains(self.rectplayer.move(1, 0)):
                self.rectplayer = self.rectplayer.move(1, 0)
                self.is_walking = True
                self.direction = 2
            else:
                self.is_walking = False
        if keys[pygame.K_LEFT]:
            if self.levelrect.contains(self.rectplayer.move(-1, 0)):
                self.rectplayer = self.rectplayer.move(-1, 0)
                self.is_walking = True
                self.direction = 3
            else:
                self.is_walking = False

    def animate(self): # Hier wird die dufte Animation gemacht
        if (time.time()-self.starttime)*1000 > self.nextframe and self.is_walking: # hier wird die Zeit seit dem Anfang des Programmstarts ausgelesen und nach 80ms der code unten ausgeführt
            self.frame = (self.frame + 1) % 4
            self.nextframe += 80
        if self.is_walking:
            self.display.blit(walkpic[self.direction][self.frame], self.rectplayer)

        else:
            self.display.blit(standpic[self.direction], self.rectplayer)

        pygame.display.flip()


def level_loop(display, player):
    display.get_imput()
    pygame.draw.rect(display.display, (0,0,0), (0, 0, 800, 800)) #Hier wird später der Hintergrund eingefügt
    player.move()
    player.animate()
    pygame.display.flip()
