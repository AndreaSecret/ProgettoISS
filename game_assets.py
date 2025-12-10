
# Informazioni generali di inizializzazione
import pyautogui
from pygame import font
from pygame.sprite import Group
font.init()
screen_x, screen_y = pyautogui.size()
screen_size = (screen_x, screen_y)
game_font = 'game_files/PixeloidSans.ttf'
turn_font = font.Font(game_font, screen_y//15)

class Game:
    def __init__(self):
        self.run = True
        self.game_start = False
        self.selected_monster = None
        self.enemy_monster = None

        self.selected_button_i = 0
        self.buttons_group = Group()
        self.active_menu = "start"

        self.turn = 0
        self.turn_surface = turn_font.render(str(self.turn), True, 'Yellow')
        self.turn_surf_pos = (screen_x-self.turn_surface.get_width()*2, self.turn_surface.get_height()//2)


    def refresh_buttons(self, new_buttons): #rimuove i bottoni attuali e li cambia in new_buttons
        self.buttons_group = Group(new_buttons)
        self.selected_button_i = 0
        new_buttons[self.selected_button_i].set_active(True)
    def switch_turn(self):
        self.active_menu = 'choose_action'
        self.selected_monster, self.enemy_monster = self.enemy_monster, self.selected_monster
        self.turn = abs(self.turn - 1)
        self.turn_surface = turn_font.render(str(self.turn), True, 'Yellow')
        return self.selected_monster.moves

game = Game()