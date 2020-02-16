import pygame

mydict = []
returnlist = []
selected_paint = 0
game_is_running = True
is_running2 = True
hoehe = 1000
breite = 1200
scale = 40
for y in range(int(1200/40)):
    for x in range(int(1200/40)):
        returnlist.append([[-1000 + x * 128, -1000 + y * 128, 128, 128], 0])

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

class Images:
    def __init__(self):
        self.images = []
        self.name = 'grass_water'
        self.backgroundrects = background_rects(scale, 1200 / scale)
    def loadimages(self):
        for i in range(10):
            a = pygame.image.load(f'Levels/parts/{self.name}/Top ({i}).png')
            self.images.append(pygame.transform.scale(a, (scale,scale)))

    def showimages(self):
        global mydict
        self.loadimages()
        for i in range(10):
            mydict[i] = [self.images[i], self.backgroundrects[i]]

def background_rects(size, anzkacheln):
    list_rect = []
    anzkacheln = int(anzkacheln)
    global mydict,returnlist
    for y in range(anzkacheln):
        for x in range(anzkacheln):
            list_rect.append(pygame.Rect((0 + x * size, 0 + y*size),(size, size)))
            a = pygame.image.load(f'Levels/parts/grass_water/Top (0).png')
            mydict.append([pygame.transform.scale(a, (scale,scale)), pygame.Rect((0 + x * size, 0 + y*size),(size, size))])

    return list_rect

class Select:
    def __init__(self, bgr, images):
        self.bgrects = bgr
        self.images = images
        self.selected = 0

    def selectedrect(self):
        global selected_paint, mydict
        if pygame.mouse.get_pressed() == (1,0,0):
            for i in self.bgrects:
                if i.collidepoint(pygame.mouse.get_pos()):
                    self.selected = self.bgrects.index(i)
                    if self.selected > 10:
                        mydict[self.selected] = [self.images[selected_paint], self.bgrects[self.selected]]
                        returnlist[self.selected][1] = selected_paint
                    elif self.selected < 10:
                        selected_paint = self.selected



screen = Display(breite, hoehe)
Allimages = Images()
Sel = Select(Allimages.backgroundrects, Allimages.images)
while game_is_running:
    Allimages.showimages()
    Sel.selectedrect()
    for i in mydict:
        screen.display.blit(i[0], i[1])
    screen.get_imput()
    pygame.display.flip()
if False: # vorsicht damit zerstörst du das alte level
    with open('Levels/Level1.txt', 'w') as filehandle:
        for listitem in returnlist:
            for i in listitem:
                filehandle.write('%s\n' % f'{i}')




