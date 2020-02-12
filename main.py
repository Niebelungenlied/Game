import pygame
import gameloop

game_is_running = True
is_running2 = True
hoehe = 1000
breite = 1200


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


screen = Display(breite, hoehe)
player = gameloop.Player(64,screen.display, (hoehe/2, breite/2))

while game_is_running:
    gameloop.level_loop(screen, player)
