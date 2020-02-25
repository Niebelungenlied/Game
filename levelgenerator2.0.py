import pygame
anzObj = 7
returnlist = []
objectlist = []
hoehe = 1000
breite = 1400
game_is_running = True
level = 1
background = pygame.image.load(f'Levels/Level{level}/bg2.png')
bgrect = background.get_rect()


class Display:  # Hier wird der screen initialisiert
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


class Images:
    def __init__(self, display):
        self.images = []
        self.name = 'grass_water'
        self.display = display
        self.guirects = []
        for x in range(2):
            for y in range(8):
                self.guirects.append(pygame.Rect(1200 + x * 64 + 2 * x, y * 64 + 2 * y, 64, 64))
        self.gui = [self.guirects, []]
        self.loadimages()

    def loadimages(self):
        for i in range(anzObj):
            a = pygame.image.load(f'Levels/Level{level}/objectsbilder/{i}.png')
            self.gui[1].append(pygame.transform.scale(a, (64, 64)))

    def showimages(self):
        for i in range(len(self.gui[1])):
            self.display.blit(self.gui[1][i], self.gui[0][i])
        for i in objectlist:
            image = self.gui[1][i[1]]
            rect = image.get_rect()
            rect.center = i[0]
            self.display.blit(image, rect)


def move():
    keys = pygame.key.get_pressed()
    global bgrect, objectlist
    if keys[pygame.K_UP]:
        bgrect = bgrect.move(0, 1)
        for i in range(len(objectlist)):
            print(objectlist[i][1])
            objectlist[i][0] = (objectlist[i][0][0] + 0, objectlist[i][0][1] + 1)

    if keys[pygame.K_DOWN]:
        bgrect = bgrect.move(0, -1)
        for i in range(len(objectlist)):
            objectlist[i][0] = (objectlist[i][0][0] + 0, objectlist[i][0][1] - 1)

    if keys[pygame.K_RIGHT]:
        bgrect = bgrect.move(1, 0)
        for i in range(len(objectlist)):
            objectlist[i][0] = (objectlist[i][0][0] + 1, objectlist[i][0][1])

    if keys[pygame.K_LEFT]:
        bgrect = bgrect.move(-1, 0)
        for i in range(len(objectlist)):
            objectlist[i][0] = (objectlist[i][0][0] - 1, objectlist[i][0][1])


class Select:
    def __init__(self, gui):
        self.gui = gui
        self.selected = 0

    def selectedrect(self):
        global objectlist
        if pygame.mouse.get_pressed() == (1, 0, 0):
            for i in self.gui[0]:
                if i.collidepoint(pygame.mouse.get_pos()):
                    self.selected = self.gui[0].index(i)
                    print(self.selected)
            if pygame.Rect(0, 0, 1200, 1000).collidepoint(pygame.mouse.get_pos()):
                objectlist.append([pygame.mouse.get_pos(), self.selected])
                print(objectlist)
                pygame.time.delay(500)


screen = Display(breite, hoehe)
images = Images(screen.display)
select = Select(images.gui)
while game_is_running:
    screen.get_imput()
    move()
    screen.display.blit(background, bgrect)
    select.selectedrect()
    images.showimages()
    pygame.display.flip()
if True:  # vorsicht damit zerstörst du das alte level
    with open(f'Levels/Level{level}/Objects.txt', 'w') as filehandle:
        for listitem in objectlist:
            for i in listitem:
                filehandle.write('%s\n' % f'{i}')
