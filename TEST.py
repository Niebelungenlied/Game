import pygame, random
import gameloop, levels, time

game_is_running = True
is_running2 = True
hoehe = 800
breite = 1200
itemsininventar = []
walkpic = standpic = bgl = []
class Dir:
    up = (0, 1)
    down = (0, -1)
    right = (-1, 0)
    left = (1, 0)


def loadcharacter(charnumb):
    global walkpic
    global standpic
    character = 'Gunter'  # Hier soll ein Charakter ausgesucht werden
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

class Display: # Hier wird der screen initialisiert
    def __init__(self, screen_size_x, screen_size_y):
        self.width = screen_size_x
        self.hight = screen_size_y
        self.display = pygame.display.set_mode((self.width, self.hight))

    def get_imput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.do_quit()
            else:
                return True

    def do_quit(self):
        global game_is_running
        global is_running2
        game_is_running = False
        is_running2 = False

class Objects:
    def __init__(self, level, display):
        self.display = display
        self.speed = 4  # Hier wird die geschwindigkeit für den Hintergrund eingerichtet
        self.rects = []
        self.images = []
        self.tuples = []
        with open(f'Levels/Level{level}/Objects.txt', 'r') as Level:
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
            self.images.append(pygame.image.load(f'Levels/Level{level}/objectsbilder/{i[1]}.png'))
            self.tuples.append((int(bgl[bgl.index(i)][0][0]), int(bgl[bgl.index(i)][0][1])))

        for i in self.images:
            self.rects.append(i.get_rect())
            self.rects[self.images.index(i)].center = self.tuples[self.images.index(i)]

    def drawobjects(self):
        for i in range(len(self.images)):
            self.display.blit(self.images[i], self.rects[i])

    def moveobjects(self, direction):
        for i in self.rects:
            self.rects[self.rects.index(i)] = i.move(int(direction[0] * self.speed), int(direction[1] * self.speed))

    def is_in_object(self, direction, rectplayer, speed):
        if rectplayer.move(direction[0] * speed, direction[1] * speed).collidelist(self.rects) == -1:
            return False
        else:
            return True

class Monster:
    def __init__(self, size, display, startpos, obj):
        loadcharacter(1)
        self.size = size
        self.lives = 7
        self.display = display
        self.objrects = obj
        self.rectplayer = pygame.Rect(0, 0, size - 15, size)
        self.rectplayer.center = startpos
        self.levelrect = pygame.Rect(200, 200, 800, 400)
        self.starttime = time.time()
        self.lasttime1 = self.lasttime2 = self.starttime
        self.nextframe = 150
        self.nextframe2 = 150
        self.nextframe3 = 150
        self.frame = 0
        self.direction = 0
        self.speeed = 100
        self.speed = 1
        self.is_walking = False
        self.is_walking2 = False
        self.objects = Objects(1, self.display)
        self.first = True
        self.last = 1

    def move(self):  # Hier wird der Spieler bewegt

        keys = pygame.key.get_pressed()
        run = False
        wait = random.randint(1000, 3000)
        if (time.time() - self.starttime) * 1000 > self.nextframe3:
            self.nextframe3 += wait
            if self.is_walking2:
                self.is_walking2 = False
            else:
                self.is_walking2 = True

        if (time.time() - self.starttime) * 1000 > self.nextframe2:
            self.nextframe2 += wait*2
            while self.direction == self.last or self.first == True:
                self.last = random.randint(0,3)
                self.first = False
            self.direction = self.last

        if self.is_walking2:
            if self.direction == 1:
                if not self.objects.is_in_object(Dir.down, self.rectplayer, self.speed):
                    if self.levelrect.move(0, -self.speed).contains(self.rectplayer.move(0, -2 * self.speed)):
                        if time.time() - self.lasttime1 > 1 / self.speeed:
                            self.lasttime1 = time.time()
                            self.rectplayer = self.rectplayer.move(0, -self.speed)
                            self.direction = 1
                    else:
                        self.direction = 0
                else:
                    self.direction = 0


                run = True

            if self.direction == 0:
                if not self.objects.is_in_object(Dir.up, self.rectplayer, self.speed):
                    if self.levelrect.contains(self.rectplayer.move(0, self.speed)):
                        if time.time() - self.lasttime1 > 1 / self.speeed:
                            self.lasttime1 = time.time()
                            self.rectplayer = self.rectplayer.move(0, self.speed)
                            self.direction = 0
                    else:
                        self.direction = 1
                else:
                    self.direction = 1
                run = True

            if self.direction == 2:
                if not self.objects.is_in_object(Dir.left, self.rectplayer, self.speed):
                    if self.levelrect.contains(self.rectplayer.move(self.speed, 0)):
                        if time.time() - self.lasttime2 > 1 / self.speeed:
                            self.lasttime2 = time.time()
                            self.rectplayer = self.rectplayer.move(self.speed, 0)
                        self.direction = 2
                    else:
                        self.direction = 3
                else:
                    self.direction = 3

                run = True

            if self.direction == 3:
                if not self.objects.is_in_object(Dir.right, self.rectplayer, self.speed):
                    if self.levelrect.contains(self.rectplayer.move(-self.speed, 0)):
                        if time.time() - self.lasttime2 > 1 / self.speeed:
                            self.lasttime2 = time.time()
                            self.rectplayer = self.rectplayer.move(-self.speed, 0)
                            self.direction = 3
                    else:
                        self.direction = 2
                else:
                    self.direction = 2

                run = True

        if run:
            self.is_walking = True
        else:
            self.is_walking = False



    def animate(self):  # Hier wird die dufte Animation gemacht
        if (time.time() - self.starttime) * 1000 > self.nextframe and self.is_walking:  # hier wird die Zeit seit dem Anfang des Programmstarts ausgelesen und nach 80ms der code unten ausgeführt
            self.frame = (self.frame + 1) % 4
            self.nextframe += 160
        if self.is_walking:
            self.display.blit(walkpic[self.direction][self.frame], self.rectplayer)

        else:
            self.display.blit(standpic[self.direction], self.rectplayer)
screen = Display(1000, 1000)
player = Player(64, screen.display, (400,400), None)
while game_is_running:
    screen.get_imput()
    player.move()
    player.animate()
    pygame.display.flip()
    pygame.time.delay(10)

