import pygame
import time
import levels

walkpic = standpic = bgl = []


class Background:
    def __init__(self, level, display):
        self.display = display
        self.bgspeed = 4 # Hier wird die geschwindigkeit für den Hintergrund eingerichtet
        self.rects = []
        self.images = []
        self.border = pygame.Rect(0, 0, 4700, 4500)  # Hier wird das riesen Rechteck festgelegt
        self.border.center = (600,500)
        with open(f'Levels/Level{level}.txt', 'r') as Level:
            test = 0
            for line in Level:
                if test % 2 == 0:
                    currentPlace = line[1:-2]
                    currentPlace = currentPlace.split(',')
                else:
                    a = line[:-1]
                    bgl.append([currentPlace, a])
                test += 1
        for i in bgl:
            self.rects.append(pygame.Rect(int(bgl[bgl.index(i)][0][0]), int(bgl[bgl.index(i)][0][1]),
                                          int(bgl[bgl.index(i)][0][2]), int(bgl[bgl.index(i)][0][3])))
            self.images.append(pygame.image.load(f'Levels/parts/grass_water/Top ({int(i[1])}).png'))
        self.topleft = (int(bgl[0][0][0]), int(bgl[0][0][1]))
        self.bottomright = (int(bgl[-1][0][0]), int(bgl[-1][0][1]))
        self.playground = pygame.Rect(0,0,1850, 2500)
        self.playground.center = (920, 600)

    def draw_background(self):
        for i in range(len(self.images)):
            self.display.blit(self.images[i], self.rects[i])
            pygame.draw.rect(self.display, (0, 0, 0), self.playground, 1)
            pygame.draw.rect(self.display, (0, 0, 0), self.border, 1)

    def movebackground(self, direction):
        self.playground = self.playground.move(direction[0] * self.bgspeed, direction[1] * self.bgspeed)
        for i in self.rects:
            self.rects[self.rects.index(i)] = i.move(direction[0] * self.bgspeed, direction[1] * self.bgspeed)

    def is_in_border(self, direction, player):
        return self.playground.contains(player.move(direction[0] * self.bgspeed*2, direction[1] * self.bgspeed*2))


class Dir:
    up = (0, 1)
    down = (0, -1)
    right = (-1, 0)
    left = (1, 0)


class Objects:
    def __init__(self, level, display):
        self.rects = levels.get_bushrects(level)
        self.display = display
        self.speed = 4

    def drawobjects(self):
        for i in self.rects:
            pygame.draw.rect(self.display, (255, 0, 0), i)


    def moveobjects(self, direction):
        for i in self.rects:
            self.rects[self.rects.index(i)] = i.move(int(direction[0] * self.speed), int(direction[1] * self.speed))

    def is_in_object(self, rectplayer, direction, speed):

        if rectplayer.move(direction[0] * speed, direction[1] * speed).collidelist(self.rects) == -1:
            return False
        else:
            return True


def loadcharacter(charnumb):
    global walkpic
    global standpic
    character = 'Character1'  # Hier soll ein Charakter ausgesucht werden
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


class Player:
    def __init__(self, size, display, startpos, obj):
        loadcharacter(1)
        self.size = size
        self.display = display
        self.objrects = obj
        self.rectplayer = pygame.Rect(0, 0, size - 15, size)
        self.rectplayer.center = startpos
        self.levelrect = pygame.Rect(200, 200, 800, 600)
        self.starttime = time.time()
        self.lasttime1 = self.lasttime2 = self.starttime
        self.nextframe = 150
        self.frame = 0
        self.direction = 0
        self.speeed = 100
        self.speed = 8
        self.is_walking = False
        self.background = Background(1, self.display)
        self.objects = Objects(1, self.display)

    def move(self):  # Hier wird der Spieler bewegt

        keys = pygame.key.get_pressed()
        run = False

        if keys[pygame.K_UP]:
            if not self.objects.is_in_object(self.rectplayer, Dir.down, self.speed):
                if self.levelrect.move(0, -self.speed).contains(self.rectplayer.move(0, -2 * self.speed)):
                    if time.time() - self.lasttime1 > 1 / self.speeed:
                        self.lasttime1 = time.time()
                        self.rectplayer = self.rectplayer.move(0, -self.speed)
                        self.direction = 1
                elif self.background.is_in_border(Dir.up, self.rectplayer):
                    self.direction = 1
                    self.objects.moveobjects(Dir.up)
                    self.background.movebackground(Dir.up)

                run = True

        if keys[pygame.K_DOWN]:
            if not self.objects.is_in_object(self.rectplayer, Dir.up, self.speed):
                if self.levelrect.contains(self.rectplayer.move(0, self.speed)):
                    if time.time() - self.lasttime1 > 1 / self.speeed:
                        self.lasttime1 = time.time()
                        self.rectplayer = self.rectplayer.move(0, self.speed)
                        self.direction = 0
                elif self.background.is_in_border(Dir.down, self.rectplayer):
                    self.direction = 0
                    self.objects.moveobjects(Dir.down)
                    self.background.movebackground(Dir.down)
                run = True

        if keys[pygame.K_RIGHT]:
            if not self.objects.is_in_object(self.rectplayer, Dir.left, self.speed):
                if self.levelrect.contains(self.rectplayer.move(self.speed, 0)):
                    if time.time() - self.lasttime2 > 1 / self.speeed:
                        self.lasttime2 = time.time()
                        self.rectplayer = self.rectplayer.move(self.speed, 0)
                    self.direction = 2
                elif self.background.is_in_border(Dir.right, self.rectplayer):
                    self.direction = 2
                    self.objects.moveobjects(Dir.right)
                    self.background.movebackground(Dir.right)

                run = True

        if keys[pygame.K_LEFT]:
            if not self.objects.is_in_object(self.rectplayer, Dir.right, self.speed):
                if self.levelrect.contains(self.rectplayer.move(-self.speed, 0)):
                    if time.time() - self.lasttime2 > 1 / self.speeed:
                        self.lasttime2 = time.time()
                        self.rectplayer = self.rectplayer.move(-self.speed, 0)
                        self.direction = 3

                elif self.background.is_in_border(Dir.left, self.rectplayer):
                    self.direction = 3
                    self.objects.moveobjects(Dir.left)
                    self.background.movebackground(Dir.left)

                run = True

        if run:
            self.is_walking = True
        else:
            self.is_walking = False

    def draw_background(self):
        self.background.draw_background()
        self.objects.drawobjects()

    def animate(self):  # Hier wird die dufte Animation gemacht
        if (time.time() - self.starttime) * 1000 > self.nextframe and self.is_walking:  # hier wird die Zeit seit dem Anfang des Programmstarts ausgelesen und nach 80ms der code unten ausgeführt
            self.frame = (self.frame + 1) % 4
            self.nextframe += 80
        if self.is_walking:
            self.display.blit(walkpic[self.direction][self.frame], self.rectplayer)

        else:
            self.display.blit(standpic[self.direction], self.rectplayer)

        pygame.display.flip()


def level_loop(display, player):
    display.get_imput()
    player.draw_background()  # Hier wird später der Hintergrund eingefügt
    player.move()
    player.animate()
    if pygame.mouse.get_pressed() == (1, 0, 0):
        print(pygame.mouse.get_pos())
        pygame.time.delay(100)
    pygame.display.flip()
