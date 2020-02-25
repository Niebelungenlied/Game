import time

import pygame
import random

import levels

itemsininventar = []
bgl = []
rectplayer = None


class Background:
    def __init__(self, level, display):
        self.display = display
        self.bgspeed = 4  # Hier wird die geschwindigkeit für den Hintergrund eingerichtet
        self.backgroundimage = pygame.image.load(f'Levels/Level{level}/bg.png')
        self.backgroundrect = self.backgroundimage.get_rect()
        self.backgroundrect.center = (920, 600)
        self.playground = pygame.Rect(0, 0, self.backgroundrect.width-420, self.backgroundrect.height-420)
        self.playground.center = (920, 600)

    def draw_background(self):
        self.display.blit(self.backgroundimage, self.backgroundrect)

    def movebackground(self, direction):
        self.playground = self.playground.move(direction[0] * self.bgspeed, direction[1] * self.bgspeed)
        self.backgroundrect = self.backgroundrect.move(direction[0] * self.bgspeed, direction[1] * self.bgspeed)

    def is_in_border(self, direction):
        return self.playground.contains(
            rectplayer.move(direction[0] * self.bgspeed , direction[1] * self.bgspeed ))


class Itemes:
    def __init__(self, level, display):
        self.display = display
        self.speed = 4  # Hier wird die geschwindigkeit für den Hintergrund eingerichtet
        self.rects = []
        self.images = []
        self.tuples = []
        lolist = []
        with open(f'Levels/Level{level}/items/items.txt', 'r') as Level:
            test = 0
            for line in Level:
                if test % 2 == 0:
                    currentPlace = line[1:-2]
                    currentPlace = currentPlace.split(',')
                else:
                    a = line[:-1]
                    lolist.append([currentPlace, a])
                test += 1
        for i in lolist:
            self.images.append(pygame.image.load(f'Levels/Level{level}/items/{i[1]}.png'))
            self.tuples.append((int(lolist[lolist.index(i)][0][0]), int(lolist[lolist.index(i)][0][1])))

        for i in self.images:
            self.rects.append(i.get_rect())
            self.rects[self.images.index(i)].center = self.tuples[self.images.index(i)]

    def draw(self):
        if len(self.rects) != 0:
            for i in range(len(self.images)):
                self.display.blit(self.images[i], self.rects[i])

    def move(self, direction, speed):
        if len(self.rects) != 0:
            for i in self.rects:
                self.rects[self.rects.index(i)] = i.move(int(direction[0] * speed), int(direction[1] * speed))

    def pickup(self):
        a = rectplayer.collidelist(self.rects)
        if a != -1:
            self.rects.pop(a)
            self.adtoinventar(a)

    def adtoinventar(self, a):
        pass


def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0]
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]
                y += word_height
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]
        y += word_height


def showE(rectobj, display):
    E = pygame.image.load(f'Levels/graphics/E.png')
    rect = E.get_rect()
    rect.bottomleft = rectobj.topright
    display.blit(E, rect)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_e]:
        return True
    else:
        return False


def showHUD(display, lives):
    lives = pygame.image.load(f'Levels/graphics/healthbar/{lives}.png')
    display.blit(lives, (1000, 0))
    showcommands(display)


def showcommands(display):
    commands = pygame.image.load(f'Levels/graphics/commands.png')
    display.blit(commands, (0, 650))
    text = "Willkommen im besten Spiel der Welt!!! \nBenutze W A S D um dich fort zu bewegen. "
    font = pygame.font.SysFont('Comic sans', 40)
    blit_text(display, text, (20, 670), font)


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

    def is_in_object(self, direction, rect, speed):
        if rect.move(direction[0] * speed, direction[1] * speed).collidelist(self.rects) == -1:
            return False
        else:
            return True


class Dir:
    up = (0, 1)
    down = (0, -1)
    right = (-1, 0)
    left = (1, 0)


class Player:
    def __init__(self, size, display, startpos, obj):
        self.is_hitting = False
        global rectplayer
        self.walkpic = levels.get_character(1, 'walk')
        self.standpic = levels.get_character(1, 'stand')
        self.hitwalkpic = levels.get_character(1, 'walk', True)
        self.hitstandpic = levels.get_character(1, 'stand', True)
        self.size = size
        self.lives = 7
        self.display = display
        self.objrects = obj
        rectplayer = self.standpic[0].get_rect()
        rectplayer.center = (700, 400)
        self.levelrect = pygame.Rect(200, 200, 800, 400)
        self.hitrangey = pygame.Rect(0, 0, 200, 200)
        self.hitrangey.size = (64, 194)
        self.hitrangex = pygame.Rect(0, 0, 200, 200)
        self.hitrangex.size = (194, 64)
        self.starttime = time.time()
        self.lasttime1 = self.lasttime2 = self.starttime
        self.nextframe = 150
        self.frame = 0
        self.direction = 0
        self.hitdirection = 0
        self.speeed = 100
        self.speed = 4
        self.is_walking = False
        self.background = Background(1, self.display)
        self.objects = Objects(1, self.display)
        self.items = Itemes(1, self.display)
        self.monster = Monster(64, self.display, self.objects)
        self.guy = [Guy(64, self.display, self.objects, pygame.Rect(600, 600, 800, 400))]
        self.pressed = False

    def check(self, direction, rect):
        a = False
        for i in self.guy:
            if i.is_in_guy(direction, rect, self.speed):
                a = True
        return a

    def move(self):  # Hier wird der Spieler bewegt
        global rectplayer
        keys = pygame.key.get_pressed()
        run = False

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if not self.objects.is_in_object(Dir.down, rectplayer, self.speed) and self.monster.is_in_monster(
                    Dir.down, rectplayer, self.speed) and self.check(Dir.down, rectplayer):
                if self.levelrect.move(0, -self.speed).contains(rectplayer.move(0, -2 * self.speed)):
                    if time.time() - self.lasttime1 > 1 / self.speeed:
                        self.lasttime1 = time.time()
                        rectplayer = rectplayer.move(0, -self.speed)
                        self.direction = 1
                elif self.background.is_in_border(Dir.up):
                    self.objects.moveobjects(Dir.up)
                    self.background.movebackground(Dir.up)
                    self.monster.movewithbg(Dir.up)
                    for i in self.guy:
                        i.movewithbg(Dir.up)
                    self.items.move(Dir.up, self.background.bgspeed)
                    self.direction = 1
                run = True
            self.hitdirection = 1


        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if not self.objects.is_in_object(Dir.up, rectplayer, self.speed) and self.monster.is_in_monster(
                    Dir.up, rectplayer, self.speed) and self.check(Dir.up, rectplayer):
                if self.levelrect.contains(rectplayer.move(0, self.speed)):
                    if time.time() - self.lasttime1 > 1 / self.speeed:
                        self.lasttime1 = time.time()
                        rectplayer = rectplayer.move(0, self.speed)
                        self.direction = 0
                elif self.background.is_in_border(Dir.down):
                    self.objects.moveobjects(Dir.down)
                    self.background.movebackground(Dir.down)
                    self.monster.movewithbg(Dir.down)
                    for i in self.guy:
                        i.movewithbg(Dir.down)
                    self.items.move(Dir.down, self.background.bgspeed)
                    self.direction = 0
                run = True
            self.hitdirection = 0


        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if not self.objects.is_in_object(Dir.left, rectplayer, self.speed) and self.monster.is_in_monster(
                    Dir.left, rectplayer, self.speed) and self.check(Dir.left, rectplayer):
                if self.levelrect.contains(rectplayer.move(self.speed, 0)):
                    if time.time() - self.lasttime2 > 1 / self.speeed:
                        self.lasttime2 = time.time()
                        rectplayer = rectplayer.move(self.speed, 0)
                        self.direction = 2
                elif self.background.is_in_border(Dir.right):
                    self.objects.moveobjects(Dir.right)
                    self.background.movebackground(Dir.right)
                    self.monster.movewithbg(Dir.right)
                    for i in self.guy:
                        i.movewithbg(Dir.right)
                    self.items.move(Dir.right, self.background.bgspeed)
                    self.direction = 2
                run = True
            self.hitdirection = 2

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if not self.objects.is_in_object(Dir.right, rectplayer, self.speed) and self.monster.is_in_monster(
                    Dir.right, rectplayer, self.speed) and self.check(Dir.right, rectplayer):
                if self.levelrect.contains(rectplayer.move(-self.speed, 0)):
                    if time.time() - self.lasttime2 > 1 / self.speeed:
                        self.lasttime2 = time.time()
                        rectplayer = rectplayer.move(-self.speed, 0)
                        self.direction = 3

                elif self.background.is_in_border(Dir.left):
                    self.objects.moveobjects(Dir.left)
                    self.background.movebackground(Dir.left)
                    self.monster.movewithbg(Dir.left)
                    for i in self.guy:
                        i.movewithbg(Dir.left)
                    self.items.move(Dir.left, self.background.bgspeed)
                    self.direction = 3
                run = True
            self.hitdirection = 3

        if keys[pygame.K_SPACE]:
            if self.pressed:
                self.hit()
                self.pressed = False
                self.is_hitting = True


        else:
            self.pressed = True
            self.is_hitting = False
        self.hitrangey.center = self.hitrangex.center = rectplayer.center
        if run:
            self.is_walking = True
        else:
            self.is_walking = False

        a = rectplayer.collidelist(self.items.rects)
        if a != -1:
            if showE(self.items.rects[a], self.display):
                self.items.pickup()

    def draw_background(self):
        self.background.draw_background()
        self.objects.drawobjects()
        self.items.draw()

    def animate(self):  # Hier wird die dufte Animation gemacht
        if (time.time() - self.starttime) * 1000 > self.nextframe and self.is_walking:  # hier wird die Zeit seit dem Anfang des Programmstarts ausgelesen und nach 80ms der code unten ausgeführt
            self.frame = (self.frame + 1) % 4
            self.nextframe += 80
        print(self.is_hitting)
        if self.is_hitting:
            if self.is_walking:
                self.display.blit(self.hitwalkpic[self.hitdirection][self.frame], rectplayer)

            else:
                self.display.blit(self.hitstandpic[self.hitdirection], rectplayer)
        else:
            if self.is_walking:
                self.display.blit(self.walkpic[self.direction][self.frame], rectplayer)

            else:
                self.display.blit(self.standpic[self.direction], rectplayer)

    def hit(self):
        if self.hitdirection == 0 and self.monster.rectmonster.colliderect(
                self.hitrangey) and self.monster.rectmonster.y > rectplayer.y:
            self.monster.takedamage(3)
        if self.hitdirection == 1 and self.monster.rectmonster.colliderect(
                self.hitrangey) and self.monster.rectmonster.y < rectplayer.y:
            self.monster.takedamage(3)
        if self.hitdirection == 2 and self.monster.rectmonster.colliderect(
                self.hitrangex) and self.monster.rectmonster.x > rectplayer.x:
            self.monster.takedamage(3)
        if self.hitdirection == 3 and self.monster.rectmonster.colliderect(
                self.hitrangex) and self.monster.rectmonster.x < rectplayer.x:
            self.monster.takedamage(3)

    def do_all(self):
        self.draw_background()
        self.move()
        self.animate()
        for i in self.guy:
            i.move()
            i.animate()

        if self.monster.health > 0:
            self.monster.move()
            self.monster.animate()


class Guy:
    def __init__(self, size, display, obj, movearea):
        self.size = size
        self.walkpic = levels.get_character(2, 'walk')
        self.standpic = levels.get_character(2, 'stand')
        self.lives = 7
        self.display = display
        self.objrects = obj
        self.rectmonster = pygame.Rect(0, 0, size - 15, size)
        self.rectmonster.center = (700, 750)
        self.moverect = movearea
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
        self.objects = obj
        self.first = True
        self.last = 1
        self.bgspeed = 4


    def move(self):  # Hier wird der Spieler bewegt

        run = False
        wait = random.randint(1000, 3000)
        if (time.time() - self.starttime) * 1000 > self.nextframe3:
            self.nextframe3 += wait
            if self.is_walking2:
                self.is_walking2 = False
            else:
                self.is_walking2 = True

        if (time.time() - self.starttime) * 1000 > self.nextframe2:
            self.nextframe2 += wait * 2
            while self.direction == self.last or self.first == True:
                self.last = random.randint(0, 3)
                self.first = False
            self.direction = self.last

        if self.is_walking2:
            if self.direction == 1:
                if not self.objects.is_in_object(Dir.down, self.rectmonster, self.speed) and self.is_in_player(Dir.down,
                                                                                                               self.speed):
                    if self.moverect.move(0, -self.speed).contains(self.rectmonster.move(0, -2 * self.speed)):
                        if time.time() - self.lasttime1 > 1 / self.speeed:
                            self.lasttime1 = time.time()
                            self.rectmonster = self.rectmonster.move(0, -self.speed)
                            self.direction = 1
                    else:
                        self.direction = 0
                else:
                    self.direction = 0

                run = True

            if self.direction == 0:
                if not self.objects.is_in_object(Dir.up, self.rectmonster, self.speed) and self.is_in_player(Dir.up,
                                                                                                             self.speed):
                    if self.moverect.contains(self.rectmonster.move(0, self.speed)):
                        if time.time() - self.lasttime1 > 1 / self.speeed:
                            self.lasttime1 = time.time()
                            self.rectmonster = self.rectmonster.move(0, self.speed)
                            self.direction = 0
                    else:
                        self.direction = 1
                else:
                    self.direction = 1
                run = True

            if self.direction == 2:
                if not self.objects.is_in_object(Dir.left, self.rectmonster, self.speed) and self.is_in_player(Dir.left,
                                                                                                               self.speed):
                    if self.moverect.contains(self.rectmonster.move(self.speed, 0)):
                        if time.time() - self.lasttime2 > 1 / self.speeed:
                            self.lasttime2 = time.time()
                            self.rectmonster = self.rectmonster.move(self.speed, 0)
                        self.direction = 2
                    else:
                        self.direction = 3
                else:
                    self.direction = 3

                run = True

            if self.direction == 3:
                if not self.objects.is_in_object(Dir.right, self.rectmonster, self.speed) and self.is_in_player(
                        Dir.right, self.speed):
                    if self.moverect.contains(self.rectmonster.move(-self.speed, 0)):
                        if time.time() - self.lasttime2 > 1 / self.speeed:
                            self.lasttime2 = time.time()
                            self.rectmonster = self.rectmonster.move(-self.speed, 0)
                            print(self.rectmonster)

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

    def do_all(self):
        self.move()
        self.animate()

    def animate(self):  # Hier wird die dufte Animation gemacht
        if (time.time() - self.starttime) * 1000 > self.nextframe and self.is_walking:  # hier wird die Zeit seit dem Anfang des Programmstarts ausgelesen und nach 80ms der code unten ausgeführt
            self.frame = (self.frame + 1) % 4
            self.nextframe += 160

        if self.is_walking:
            self.display.blit(self.walkpic[self.direction][self.frame], self.rectmonster)

        else:
            self.display.blit(self.standpic[self.direction], self.rectmonster)

    def movewithbg(self, direction):
        self.rectmonster = self.rectmonster.move(direction[0] * self.bgspeed, direction[1] * self.bgspeed)
        self.moverect = self.moverect.move(direction[0] * self.bgspeed, direction[1] * self.bgspeed)

    def is_in_player(self, direction, speed):
        if self.rectmonster.move(direction[0] * speed, direction[1] * speed).colliderect(rectplayer):

            return False
        else:
            return True

    def is_in_guy(self, direction, rect, speed):
        if rect.move(direction[0] * speed, direction[1] * speed).colliderect(self.rectmonster):

            return False
        else:
            return True


class Monster:
    def __init__(self, size, display, obj):
        self.walkpic = levels.get_character(3, 'walk')
        self.standpic = levels.get_character(3, 'stand')
        self.size = size
        self.lives = 7
        self.display = display
        self.objrects = obj
        self.rectmonster = pygame.Rect(0, 0, size - 15, size)
        self.rectmonster.center = (400, 400)
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
        self.objects = obj
        self.first = True
        self.last = 1
        self.bgspeed = 4
        self.health = 10

    def move(self):  # Hier wird der Spieler bewegt
        run = False
        self.is_walking2 = True
        if self.is_walking2:
            if rectplayer.y < self.rectmonster.y:
                if not self.objects.is_in_object(Dir.down, self.rectmonster, self.speed) and self.is_in_player(Dir.down,
                                                                                                               self.speed):
                    print('1')
                    if self.levelrect.move(0, -self.speed).contains(self.rectmonster.move(0, -2 * self.speed)):
                        print('2')
                        if time.time() - self.lasttime1 > 1 / self.speeed:
                            print('3')
                            self.lasttime1 = time.time()
                            self.rectmonster = self.rectmonster.move(0, -self.speed)
                            self.direction = 1

                    else:
                        self.direction = 0
                else:
                    self.direction = 0

                run = True

            if rectplayer.y > self.rectmonster.y:
                if not self.objects.is_in_object(Dir.up, self.rectmonster, self.speed) and self.is_in_player(Dir.up,
                                                                                                             self.speed):
                    if self.levelrect.contains(self.rectmonster.move(0, self.speed)):
                        if time.time() - self.lasttime1 > 1 / self.speeed:
                            self.lasttime1 = time.time()
                            self.rectmonster = self.rectmonster.move(0, self.speed)
                            self.direction = 0
                    else:
                        self.direction = 1
                else:
                    self.direction = 1
                run = True

            if rectplayer.x > self.rectmonster.x:
                if not self.objects.is_in_object(Dir.left, self.rectmonster, self.speed) and self.is_in_player(Dir.left,
                                                                                                               self.speed):
                    if self.levelrect.contains(self.rectmonster.move(self.speed, 0)):
                        if time.time() - self.lasttime2 > 1 / self.speeed:
                            self.lasttime2 = time.time()
                            self.rectmonster = self.rectmonster.move(self.speed, 0)
                        self.direction = 2
                    else:
                        self.direction = 3
                else:
                    self.direction = 3

                run = True

            if rectplayer.x < self.rectmonster.x:
                if not self.objects.is_in_object(Dir.right, self.rectmonster, self.speed) and self.is_in_player(
                        Dir.right, self.speed):
                    if self.levelrect.contains(self.rectmonster.move(-self.speed, 0)):
                        if time.time() - self.lasttime2 > 1 / self.speeed:
                            self.lasttime2 = time.time()
                            self.rectmonster = self.rectmonster.move(-self.speed, 0)
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

    def do_all(self):
        self.move()
        self.animate()

    def animate(self):  # Hier wird die dufte Animation gemacht
        if (time.time() - self.starttime) * 1000 > self.nextframe and self.is_walking:  # hier wird die Zeit seit dem Anfang des Programmstarts ausgelesen und nach 80ms der code unten ausgeführt
            self.frame = (self.frame + 1) % 4
            self.nextframe += 160
        if self.is_walking:
            self.display.blit(self.walkpic[self.direction][self.frame], self.rectmonster)

        else:
            self.display.blit(self.standpic[self.direction], self.rectmonster)

    def movewithbg(self, direction):
        self.rectmonster = self.rectmonster.move(direction[0] * self.bgspeed, direction[1] * self.bgspeed)
        self.levelrect = self.levelrect.move(direction[0] * self.bgspeed, direction[1] * self.bgspeed)

    def is_in_player(self, direction, speed):
        if self.rectmonster.move(direction[0] * speed, direction[1] * speed).colliderect(rectplayer):

            return False
        else:
            return True

    def is_in_monster(self, direction, rect, speed):
        if rect.move(direction[0] * speed, direction[1] * speed).colliderect(self.rectmonster):

            return False
        else:
            return True

    def takedamage(self, damage):
        self.health -= damage
        print(self.health)


def level_loop(display, player):
    display.get_imput()
    player.do_all()
    showHUD(display.display, player.lives)
    pygame.display.flip()
