import pygame
import time

game_is_running = True
is_running2 = True
hoehe = 800
breite = 800


class Display:
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


clock = pygame.time.Clock()
screen = Display(breite, hoehe)

while game_is_running:
    screen.get_imput()
    pygame.draw.rect(screen.display, (255, 0, 0), ((0, 0), (200, 400)))
    pygame.display.flip()
