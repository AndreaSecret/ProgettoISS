# Informazioni generali di inizializzazione
from pyautogui import size
from pygame import font
from pygame.sprite import Group
from pygame.surface import Surface
font.init()
screen_x, screen_y = size()
screen_size = (screen_x, screen_y)
game_font = 'game_files/PixeloidSans.ttf'
turn_font = font.Font(game_font, screen_y//15)

bar_h = screen_y/4 #altezza della barra sotto
monster_size = round(screen_y/2.7) #dimensione sprite mostri selezionati
monster_size = (monster_size, monster_size)
attacking_monster_pos = (screen_x/5,screen_y/2)
defending_monster_pos = (screen_x*4/5-monster_size[0],screen_y/6)

# titolo "choose team limit"
choose_tl_title_font = font.Font(game_font, screen_y//15)
choose_tl_title_surface = choose_tl_title_font.render('Scegliere numero componenti team', True, (255, 255, 255))
choose_tl_title_pos = ((screen_x - choose_tl_title_surface.get_width())/2,screen_y//50)

# descrizione mossa selezionata
move_desc_font = font.Font(game_font, int(bar_h/7))
move_desc_pos_x = screen_x*3/5
move_desc_padding_y = bar_h/20

# game core

class Game:
    def __init__(self):
        self.team_limit = 0 #numero massimo di mostri in squadra, viene scelto nella scheramata choose_team_limit
        self.max_xp = 3
        self.plus_moves_duration = 2 # turni di durata delle mosse plus

        self.teams = {0: [],
                      1: []}
        self.team_colors = {
            0 : (0,0,255),
            1 : (255,0,0)
        }
        self.teams_xp = {0: 0,
                         1: 0}
        self.active_plus_durations = {0 : 0,
                                     1 : 0}

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

        self.move_desc_surf = Surface((bar_h*1.5, bar_h))
        self.generated_move_desc = None # variabile utile per evitare di calcolare la descrizione ogni frame

    def set_initiation(self, menu_layouts, VisualMonsterClass, animation_manager, bar, selected_box, enemy_box, selected_infobox, enemy_infobox):
        self.MENU_LAYOUT = menu_layouts
        self.game_start = True
        self.visualMonsterClass = VisualMonsterClass
        self.animation_manager = animation_manager
        self.game_bar = bar
        self.selected_box = selected_box
        self.enemy_box = enemy_box
        self.box_group = Group(self.selected_box, self.enemy_box)
        self.selected_infobox = selected_infobox
        self.enemy_infobox = enemy_infobox
        self.infobox_group = Group(self.selected_infobox, self.enemy_infobox)

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
        self.refresh_boxes()

    def refresh_buttons(self, new_buttons): #rimuove i bottoni attuali e li cambia in new_buttons
        self.buttons_group = Group(new_buttons)
        self.selected_button_i = 0
        new_buttons[self.selected_button_i].set_active(True)

    def refresh_moves(self):
        self.MENU_LAYOUT.update_moves_buttons()
        self.active_menu = 'choose_action'
        self.refresh_buttons(self.MENU_LAYOUT['choose_action']['buttons'])

    def refresh_boxes(self): # funzione che si occupa di aggiornare le due box con le info dei mostri
        self.selected_box.set_monster(self.selected_monster)
        self.selected_infobox.set_monster(self.selected_monster)
        self.enemy_box.set_monster(self.enemy_monster)
        self.enemy_infobox.set_monster(self.enemy_monster)

    def switch_turn_number(self):
        self.turn = abs(self.turn - 1)
        self.turn_surface = turn_font.render(str(self.turn+1), True, self.team_colors[self.turn])

    def switch_turn(self):
        self.selected_monster, self.enemy_monster = self.enemy_monster, self.selected_monster
        self.update_status_effects()
        self.refresh_boxes()

        if self.selected_monster.alive:
            self.active_menu = 'choose_action'
        else: # se il mostro è stato ucciso, ne fa scegliere un altro
            self.active_menu = 'change_monster'
            self.MENU_LAYOUT.update_change_monster_buttons(force_change=True)
            self.refresh_buttons(self.MENU_LAYOUT['change_monster']['buttons'])

        self.switch_turn_number()
        self.MENU_LAYOUT.update_moves_buttons()
    
    def update_status_effects(self):
        for monster in self.teams[0]:
            monster.update_status_effects()
        for monster in self.teams[1]:
            monster.update_status_effects()

    def switch_monster(self, monster):
        self.selected_monster = monster
        self.selected_monster_sprite.change_monster(monster)
        self.refresh_boxes()

    def generate_move_desc(self, move):
        self.move_desc_surf.fill('White')
        if not move: # è nel tasto indietro
            return move_desc_font.render('', True, (255, 255, 255))
        move_desc_text = ''+str(move.power)
        match move.type:
            case 'attack':
                move_desc_text+=' danno a'
            case 'heal':
                move_desc_text+=' cura a'
            case 'buff' | 'debuff':
                if move.type == 'debuff': move_desc_text='-'+move_desc_text
                else: move_desc_text='+'+move_desc_text
                move_desc_text+='%'
                match move.status_effect.targeted_stat:
                    case 'attack':
                        move_desc_text+=' attacco a'
                    case 'defense':
                        move_desc_text+=' difesa a'
        
        if move.choose_target:
            move_desc_text+='d un alleato a scelta'
        else:
            if move.target == 'to_other':
                move_desc_text+='l nemico'
            else:
                move_desc_text+=' se stesso'
        if move.type == 'buff' or move.type == 'debuff':
            move_desc_text+=' per '+str(move.status_effect.duration)+' turni.'
        else:
            move_desc_text+='.'

        # plus moves
        if move.is_plus:
            match move.plus_type:
                case 'heal':
                    move_desc_text += ' Cura inoltre se stesso di '+str(move.heal_amount)+'.'
                case 'damage':
                    move_desc_text += ' Inoltre fa '+str(move.dmg_amount)+' al nemico.'
                case 'debuff':
                    move_desc_text += ' Inoltre '+str(move.plus_status_effect.power)+'%'
                    match move.plus_status_effect.targeted_stat:
                        case 'attack':
                            move_desc_text+=' attacco al nemico.'
                        case 'defense':
                            move_desc_text+=' difesa al nemico.'
                case 'buff':
                    move_desc_text += ' Inoltre +'+str(move.plus_status_effect.power)+'%'
                    match move.plus_status_effect.targeted_stat:
                        case 'attack':
                            move_desc_text+=' attacco a se stesso.'
                        case 'defense':
                            move_desc_text+=' difesa a se stesso.'
                case 'remove_debuffs':
                    move_desc_text += ' Inoltre rimuove i propri debuff.'


        # text wrapping
        words = move_desc_text.split(' ')
        lines = []
        current_line = ''

        for word in words:
            test_line = current_line + (' ' if current_line else '') + word
            if move_desc_font.size(test_line)[0] <= self.move_desc_surf.get_width():
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        # trovo le posizioni delle lines
        text_h = move_desc_font.size(test_line)[1]
        total_h = len(lines)*text_h + (len(lines)-1)*move_desc_padding_y
        y =  (bar_h - total_h) / 2
        for line in lines:
            text = move_desc_font.render(line, True, (0,0,0))
            x= (self.move_desc_surf.get_width()-text.get_width())/2
            self.move_desc_surf.blit(text, (x,y))
            y+=text_h+move_desc_padding_y
        self.generated_move_desc = move

    def update(self, display, background): # chiamata ogni frame
        if self.game_start:
            if self.match_start:
                display.blit(background, (0,0))

                self.animation_manager.update()
                self.is_in_animation = True if self.animation_manager.current else False
            
                self.selected_monster_sprite.update(display)
                self.enemy_monster_sprite.update(display)

                self.game_bar.draw(display)
                self.box_group.update()
                if self.animation_manager.current!='switching_sides':
                    self.box_group.draw(display)

            display.blit(self.turn_surface, self.turn_surf_pos)

        if self.active_menu == 'choose_team_limit':
            display.blit(choose_tl_title_surface, choose_tl_title_pos)
        elif self.active_menu == 'choose_move':
            self.infobox_group.draw(display)
            selected_move = getattr(self.MENU_LAYOUT['choose_move']['buttons'][self.selected_button_i].action, 'move', None)
            if selected_move != self.generated_move_desc: self.generate_move_desc(selected_move)
            display.blit(self.move_desc_surf, (move_desc_pos_x, screen_y-bar_h))

game = Game()
