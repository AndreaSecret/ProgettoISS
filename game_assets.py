
# Informazioni generali di inizializzazione
import pyautogui
from pygame import font
from pygame.sprite import Group
font.init()
screen_x, screen_y = pyautogui.size()
screen_size = (screen_x, screen_y)
game_font = 'game_files/PixeloidSans.ttf'
turn_font = font.Font(game_font, screen_y//15)

# game core

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

        self.animation_manager = None
        self.is_in_animation = False

    def start_game(self, selected_monster, enemy_monster, VisualMonsterClass, animation_manager):
        self.game_start = True
        self.active_menu = 'choose_action'

        self.selected_monster = selected_monster
        self.enemy_monster = enemy_monster
        self.selected_monster_sprite = VisualMonsterClass(self.selected_monster, attacking_monster_pos, 'attacking')
        self.enemy_monster_sprite = VisualMonsterClass(self.enemy_monster, defending_monster_pos, 'defending')

        self.animation_manager = animation_manager

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

    def update(self, display):
        self.animation_manager.update()
        self.is_in_animation = True if self.animation_manager.current else False

        self.selected_monster_sprite.update(display)
        self.enemy_monster_sprite.update(display)

        display.blit(self.turn_surface, self.turn_surf_pos)

game = Game()

# altre costanti di inizializzazione:

monster_size = (400,400)
attacking_monster_pos = (screen_x/5,screen_y/2)
defending_monster_pos = (screen_x*4/5-monster_size[0],screen_y/6)