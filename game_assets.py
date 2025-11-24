
# Informazioni generali di inizializzazione

from pygame import font
font.init()

class Game:
    def __init__(self):
        self.run = True
game = Game()

screen_size = (1000, 600)
game_font = font.SysFont('Comic Sans MS', 30)