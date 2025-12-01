
# Informazioni generali di inizializzazione

from pygame import font
font.init()

class Game:
    def __init__(self):
        self.run = True
        self.selected_button_i = 0
game = Game()

screen_size = (1000, 600)
game_font = font.SysFont('Comic Sans MS', 30)