
# Informazioni generali di inizializzazione
import pyautogui
from pygame import font, init
from pygame.sprite import Group
init()
screen_x, screen_y = pyautogui.size()
class Game:
    def __init__(self):
        self.run = True
        self.selected_button_i = 0
        self.buttons = []
        self.buttons_group = Group()
        self.start_menu = True
        self.game_start = False
        self.choose_action_menu = False
        self.choose_move_menu = False

    def refresh_buttons(self, new_buttons): #rimuove i bottoni attuali e li cambia in new_buttons
        self.buttons = new_buttons
        self.buttons_group.empty()
        self.buttons_group.add(self.buttons)
        self.selected_button_i = 0
        self.buttons[self.selected_button_i].set_active(True)

game = Game()

screen_size = (screen_x, screen_y)
game_font = font.SysFont('Comic Sans MS', 30)