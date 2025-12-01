
# Informazioni generali di inizializzazione

from pygame import font, display, init
init()
infoObject = display.Info()
screen_x, screen_y = infoObject.current_w, infoObject.current_h

class Game:
    def __init__(self):
        self.run = True
        self.selected_button_i = 0
        self.start_menu = True
        self.game_start = False
game = Game()

screen_size = (screen_x, screen_y)
game_font = font.SysFont('Comic Sans MS', 30)