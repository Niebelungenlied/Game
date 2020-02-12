hoehe = 800
breite = 800


def get_character(characternumber):
    if characternumber == 1:
        return 'Character1'





class Level:
    def __init__(self, level):
        self.level = level

    def get_background(self):
        if self.level == 1:
            return 'bg.png'