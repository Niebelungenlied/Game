import pygame
import time
import levels

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
        self.rectplayer = pygame.Rect(0, 0, size, size)
        self.rectplayer.center = startpos
        self.backgroundpic = pygame.image.load(f'Levels/{levels.get_background(1)}')
        self.backgroundrect = self.backgroundpic.get_rect()
        self.backgroundrect.center = (600, 500)
        self.levelrect = pygame.Rect(200, 200, 800, 600)
        self.starttime = time.time()
        self.lasttime1 = self.lasttime2 = self.starttime
        self.nextframe = 80
        self.frame = 0
        self.direction = 0
        self.speeed = 200
        self.speed = 2
        self.is_walking = False
        self.bgspeed = 2


    def move(self):  # Hier wird der Spieler bewegt
        keys = pygame.key.get_pressed()
        run = False
        if keys[pygame.K_UP]:
            if self.levelrect.contains(self.rectplayer.move(0, -self.speed)):
                if time.time() - self.lasttime1 > 1 / self.speeed:
                    self.lasttime1 = time.time()
                    self.rectplayer = self.rectplayer.move(0, -self.speed)
                    self.direction = 1
            else:
                self.backgroundrect = self.backgroundrect.move(0, self.bgspeed)
            run = True

        if keys[pygame.K_DOWN]:
            if self.levelrect.contains(self.rectplayer.move(0, self.speed)):
                if time.time() - self.lasttime1 > 1 / self.speeed:
                    self.lasttime1 = time.time()
                    self.rectplayer = self.rectplayer.move(0, self.speed)
                    self.direction = 0
            else:
                self.backgroundrect = self.backgroundrect.move(0, -self.bgspeed)
            run = True


        if keys[pygame.K_RIGHT]:
            if self.levelrect.contains(self.rectplayer.move(self.speed, 0)):
                if time.time() - self.lasttime2 > 1 / self.speeed:
                    self.lasttime2 = time.time()
                    self.rectplayer = self.rectplayer.move(self.speed, 0)
                self.direction = 2
            else:
                self.backgroundrect = self.backgroundrect.move(-self.bgspeed, 0)
            run = True

        if keys[pygame.K_LEFT]:
            if self.levelrect.contains(self.rectplayer.move(-self.speed, 0)):
                if time.time() - self.lasttime2 > 1 / self.speeed:
                    self.lasttime2 = time.time()
                    self.rectplayer = self.rectplayer.move(-self.speed, 0)
                    self.direction = 3

            else:
                self.backgroundrect = self.backgroundrect.move(self.bgspeed, 0)
            run = True

        if run:
            self.is_walking = True
        else:
            self.is_walking = False

    def draw_background(self):
        self.display.blit(self.backgroundpic, self.backgroundrect)
        print(self.backgroundrect)


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
    player.draw_background() #Hier wird später der Hintergrund eingefügt
    player.move()
    player.animate()
    pygame.display.flip()
