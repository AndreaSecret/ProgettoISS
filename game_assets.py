
# Informazioni generali di inizializzazione
import pyautogui
from pygame import font, init
init()
screen_x, screen_y = pyautogui.size()
print(screen_x,screen_y)


class Game:
    def __init__(self):
        self.run = True
        self.selected_button_i = 0
        self.start_menu = True
        self.game_start = False
game = Game()

screen_size = (screen_x, screen_y)
game_font = font.SysFont('Comic Sans MS', 30)