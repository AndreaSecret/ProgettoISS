
# Informazioni generali di inizializzazione
import pyautogui
from pygame import font
from pygame.sprite import Group
font.init()
screen_x, screen_y = pyautogui.size()
screen_size = (screen_x, screen_y)
game_font = 'game_files/PixeloidSans.ttf'
turn_font = font.Font(game_font, screen_y//15)

monster_size = round(screen_y/2.7) #dimensione sprite mostri selezionati
monster_size = (monster_size, monster_size)
attacking_monster_pos = (screen_x/5,screen_y/2)
defending_monster_pos = (screen_x*4/5-monster_size[0],screen_y/6)

# game core

class Game:
    def __init__(self):
        self.team_limit = 3 #numero massimo di mostri in squadra
        self.teams = {0: [],
                      1: []}
        self.team_colors = {
            0 : (0,0,255),
            1 : (255,0,0)
        }

        self.run = True # se l'applicazione è avviata
        self.game_start = False # se è iniziata la partita 
        self.match_start = False # se è iniziata la battaglia (quindi draft escluso)
        self.selected_monster = None
        self.enemy_monster = None

        self.selected_button_i = 0
        self.buttons_group = Group()
        self.active_menu = "start"

        self.turn = 0
        self.turn_surface = turn_font.render(str(self.turn+1), True, self.team_colors[self.turn])
        self.turn_surf_pos = (screen_x-self.turn_surface.get_width()*2, self.turn_surface.get_height()//2)

        self.animation_manager = None
        self.is_in_animation = False

    def add_monster_to_team(self, monster):
        self.teams[self.turn].append(monster)

        self.switch_turn_number()
        if len(self.teams[0]) == len(self.teams[1]) == self.team_limit:
            self.match_start = True
            self.start_match()

    def set_initiation(self, VisualMonsterClass, animation_manager, bar):
        self.game_start = True
        self.visualMonsterClass = VisualMonsterClass
        self.animation_manager = animation_manager
        self.game_bar = bar

    def start_match(self):
        self.match_start = True
        self.active_menu = 'choose_action'

        self.selected_monster = self.teams[0][0]
        self.enemy_monster = self.teams[1][0]
        self.selected_monster_sprite = self.visualMonsterClass(self.selected_monster, attacking_monster_pos, 'attacking')
        self.enemy_monster_sprite = self.visualMonsterClass(self.enemy_monster, defending_monster_pos, 'defending')

    def refresh_buttons(self, new_buttons): #rimuove i bottoni attuali e li cambia in new_buttons
        self.buttons_group = Group(new_buttons)
        self.selected_button_i = 0
        new_buttons[self.selected_button_i].set_active(True)

    def switch_turn_number(self):
        self.turn = abs(self.turn - 1)
        self.turn_surface = turn_font.render(str(self.turn+1), True, self.team_colors[self.turn])

    def switch_turn(self):
        self.active_menu = 'choose_action'
        self.selected_monster, self.enemy_monster = self.enemy_monster, self.selected_monster
        self.switch_turn_number()
        return self.selected_monster.moves

    def update(self, display):
        if self.match_start:
            self.animation_manager.update()
            self.is_in_animation = True if self.animation_manager.current else False
        
            self.selected_monster_sprite.update(display)
            self.enemy_monster_sprite.update(display)

            self.game_bar.draw(display)

        display.blit(self.turn_surface, self.turn_surf_pos)

game = Game()
