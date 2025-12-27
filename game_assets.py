# Informazioni generali di inizializzazione
import pyautogui
from pygame import font
from pygame.sprite import Group
font.init()
screen_x, screen_y = pyautogui.size()
screen_size = (screen_x, screen_y)
game_font = 'game_files/PixeloidSans.ttf'
turn_font = font.Font(game_font, screen_y//15)

bar_h = screen_y/4 #altezza della barra sotto
monster_size = round(screen_y/2.7) #dimensione sprite mostri selezionati
monster_size = (monster_size, monster_size)
attacking_monster_pos = (screen_x/5,screen_y/2)
defending_monster_pos = (screen_x*4/5-monster_size[0],screen_y/6)

choose_tl_title_font = font.Font(game_font, screen_y//15)
choose_tl_title_surface = choose_tl_title_font.render('Scegliere numero componenti team', True, (255, 255, 255))
choose_tl_title_pos = ((screen_x - choose_tl_title_surface.get_width())/2,screen_y//50)

# game core

class Game:
    def __init__(self):
        self.team_limit = 0 #numero massimo di mostri in squadra (CAMBIABILE DA 1 A 6!!!)
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

    def set_initiation(self, menu_layouts, VisualMonsterClass, animation_manager, bar, selected_box, enemy_box):
        self.MENU_LAYOUT = menu_layouts
        self.game_start = True
        self.visualMonsterClass = VisualMonsterClass
        self.animation_manager = animation_manager
        self.game_bar = bar
        self.selected_box = selected_box
        self.enemy_box = enemy_box
        self.box_group = Group(self.selected_box, self.enemy_box)

    def add_monster_to_team(self, monster):
        self.teams[self.turn].append(monster)

        self.switch_turn_number()
        if len(self.teams[0]) == len(self.teams[1]) == self.team_limit:
            self.match_start = True
            self.start_match()

    def remove_monster_from_team(self, monster): #quando un mostro muore
        self.teams[monster.team].remove(monster)

        if len(self.teams[monster.team])==0:
            print(f'Giocatore {str(abs(self.turn)+1)} vince')
            self.run = False

    def start_match(self):
        self.match_start = True
        self.active_menu = 'choose_action'

        self.selected_monster = self.teams[0][0]
        self.enemy_monster = self.teams[1][0]
        self.selected_monster_sprite = self.visualMonsterClass(self.selected_monster, attacking_monster_pos, 'attacking')
        self.enemy_monster_sprite = self.visualMonsterClass(self.enemy_monster, defending_monster_pos, 'defending')
        self.selected_box.set_monster(self.selected_monster)
        self.enemy_box.set_monster(self.enemy_monster)

    def refresh_buttons(self, new_buttons): #rimuove i bottoni attuali e li cambia in new_buttons
        self.buttons_group = Group(new_buttons)
        self.selected_button_i = 0
        new_buttons[self.selected_button_i].set_active(True)

    def refresh_moves(self):
        self.MENU_LAYOUT.update_moves_buttons()
        self.active_menu = 'choose_action'
        self.refresh_buttons(self.MENU_LAYOUT['choose_action']['buttons'])

    def switch_turn_number(self):
        self.turn = abs(self.turn - 1)
        self.turn_surface = turn_font.render(str(self.turn+1), True, self.team_colors[self.turn])

    def switch_turn(self):
        self.selected_monster, self.enemy_monster = self.enemy_monster, self.selected_monster
        self.selected_box.set_monster(self.selected_monster)
        self.enemy_box.set_monster(self.enemy_monster)
        if self.selected_monster.alive:
            self.active_menu = 'choose_action'
        else:
            self.active_menu = 'change_monster'
            self.MENU_LAYOUT.update_change_monster_buttons(force_change=True)
            self.refresh_buttons(self.MENU_LAYOUT['change_monster']['buttons'])

        self.MENU_LAYOUT.update_moves_buttons()
        self.switch_turn_number()

    def switch_monster(self, monster):
        self.selected_monster = monster
        self.selected_monster_sprite.change_monster(monster)
        self.selected_box.set_monster(self.selected_monster)

    def update(self, display):
        if self.active_menu == 'choose_team_limit':
            display.blit(choose_tl_title_surface, choose_tl_title_pos)

        if self.game_start:
            if self.match_start:
                self.animation_manager.update()
                self.is_in_animation = True if self.animation_manager.current else False
            
                self.selected_monster_sprite.update(display)
                self.enemy_monster_sprite.update(display)

                self.game_bar.draw(display)
                self.box_group.update()
                if self.animation_manager.current!='switching_sides':
                    self.box_group.draw(display)

            display.blit(self.turn_surface, self.turn_surf_pos)

game = Game()
