# file per i tasti
from abc import ABC, abstractmethod
import pygame
from random import choices
from game_assets import game, screen_size, screen_x, screen_y, game_font, bar_h
from monsters import monster_factory, MONSTERS
from Monsters_sprites import VisualMonster
from animations import animation_manager
from bar_menu import bar, defending_monster_box, attacking_monster_box, attacking_monster_infobox, defending_monster_infobox
from numpy import stack, float32, uint8

#button action functions

class ButtonAction(ABC):
    @abstractmethod
    def execute(self):
        pass


class PlayAction(ButtonAction):
    def execute(self):
        game.active_menu = 'choose_team_limit'
        new_buttons = button_factory.create_choose_team_limit_buttons()
        MENU_LAYOUTS.update_menu_buttons('choose_team_limit', new_buttons)
        game.refresh_buttons(MENU_LAYOUTS['choose_team_limit']['buttons'])

class ExitAction(ButtonAction):
    def __init__(self, game):
        self.game = game

    def execute(self):
        self.game.run = False

class SetTeamLimitAction(ButtonAction):
    def __init__(self, number):
        self.number = number
    def execute(self):
        game.team_limit = self.number
        MENU_LAYOUTS['change_monster']['cols'] = self.number
        start_draft()

def start_draft(): #inizio draft
    game.set_initiation(MENU_LAYOUTS, VisualMonster, animation_manager, bar, attacking_monster_box, defending_monster_box, attacking_monster_infobox, defending_monster_infobox)

    monsters_names = choices(list(MONSTERS.keys()), k=12) #scelgo 12 mostri a caso
    imgs = [MONSTERS[monster]['front'].copy() for monster in monsters_names]
    monsters = zip(monsters_names, imgs)
    draft_buttons = button_factory.create_draft_buttons(monsters) #genero i bottoni dei mostri
    MENU_LAYOUTS.update_menu_buttons('draft', draft_buttons)

    game.active_menu = 'draft'
    game.refresh_buttons(MENU_LAYOUTS['draft']['buttons'])

class ChooseDraft(ButtonAction):
    def __init__(self, monster_name):
        self.monster_name = monster_name
    def execute(self):
        #crea l'entità mostro e lo aggiunge al team
        monster = monster_factory.create_monster(self.monster_name, game.turn)
        game.add_monster_to_team(monster)
        if game.match_start: #se i team sono completi, inizia la battaglia
            new_moves = button_factory.create_move_buttons(game.selected_monster.moves)
            MENU_LAYOUTS.update_menu_buttons('choose_move', new_moves)
            game.refresh_buttons(MENU_LAYOUTS['choose_action']['buttons'])
        else: #sennò procede con la selezione del prossimo mostro
            game.selected_button_i = 0
            MENU_LAYOUTS[game.active_menu]['buttons'][game.selected_button_i].set_active(True)

class ChangeMonster(ButtonAction):
    def execute(self):
        game.active_menu = 'change_monster'
        MENU_LAYOUTS.update_change_monster_buttons()
        game.refresh_buttons(MENU_LAYOUTS['change_monster']['buttons'])

class Back_to_choose_action(ButtonAction):
    def execute(self):
        game.active_menu = 'choose_action'
        game.refresh_buttons(MENU_LAYOUTS['choose_action']['buttons'])

class ChooseMonster(ButtonAction):
    def __init__(self, monster):
        self.monster = monster
    def execute(self):
        game.switch_monster(self.monster)
        game.active_menu = 'choose_action'
        game.refresh_moves()

class ChooseMove(ButtonAction):
    def execute(self):
        game.active_menu = 'choose_move'
        game.refresh_buttons(MENU_LAYOUTS['choose_move']['buttons'])
        # in questo caso seleziono il secondo tasto al posto del primo (Non seleziono 'Indietro')
        MENU_LAYOUTS[game.active_menu]['buttons'][game.selected_button_i].set_active(False)
        game.selected_button_i=1
        MENU_LAYOUTS[game.active_menu]['buttons'][game.selected_button_i].set_active(True)

class UseMove(ButtonAction):
    def __init__(self, move):
        self.move = move

    def execute(self):
        game.animation_manager.add_attack_anim(game.selected_monster_sprite, game.enemy_monster, self.move)
        game.animation_manager.add_switching_sides_anim(game.selected_monster_sprite, game.enemy_monster_sprite, game.switch_turn)
        game.active_menu = 'choose_action'
        game.refresh_buttons(MENU_LAYOUTS['choose_action']['buttons'])


class ButtonFactory:
    def __init__(self, screen_size, main_menu_button_size, moves_button_size, draft_button_size, font):
        self.screen_size = screen_size
        self.main_menu_button_size = main_menu_button_size
        self.moves_button_size = moves_button_size
        self.draft_button_size = draft_button_size
        self.font = font
        self.inactive_main_menu_color = "#FFFF01"
        self.active_main_menu_color = "#FF8801"
        self.inactive_move_color = "#BFE6EA"
        self.active_move_color = "#358FC7"

    def create_menu_button(self, text, x, y, action):
        return Button(text, (x, y), self.main_menu_button_size, action, self.font, self.inactive_main_menu_color, self.active_main_menu_color)
    
    def create_move_buttons(self, moves: list):
        moves_padding = screen_y/40
        bar_y = screen_y - bar_h
        # Tasto Indietro
        x0,y0 = moves_padding, (screen_y-bar_y)/2-self.moves_button_size[1]/2+bar_y
        back_button = Button('Indietro', (x0, y0), self.moves_button_size, Back_to_choose_action(), self.font, self.inactive_move_color, self.active_move_color)
        # posizioni dei 4 bottoni delle mosse:
        x1,y1 = moves_padding*2+self.moves_button_size[0], bar_y+moves_padding
        x2,y2 = moves_padding*3+self.moves_button_size[0]*2, bar_y+moves_padding
        x3,y3 = moves_padding*2+self.moves_button_size[0], bar_y+moves_padding*2+self.moves_button_size[1]
        x4,y4 = moves_padding*3+self.moves_button_size[0]*2, bar_y+moves_padding*2+self.moves_button_size[1]

        mossa1 = Button(moves[0].name, (x1, y1), self.moves_button_size, UseMove(moves[0]), self.font, self.inactive_move_color, self.active_move_color)
        mossa2 = Button(moves[1].name, (x2, y2), self.moves_button_size, UseMove(moves[1]), self.font, self.inactive_move_color, self.active_move_color)
        mossa3 = Button(moves[2].name, (x3, y3), self.moves_button_size, UseMove(moves[2]), self.font, self.inactive_move_color, self.active_move_color)
        mossa4 = Button(moves[3].name, (x4, y4), self.moves_button_size, UseMove(moves[3]), self.font, self.inactive_move_color, self.active_move_color)

        return [back_button,mossa1,mossa2,back_button,mossa3,mossa4]
    
    def create_draft_buttons(self, monsters : zip):
        monsters = list(monsters)
        button_side = self.draft_button_size[0] #tanto è un quadrato
        draft_x_padding = (screen_x-button_side*6)/7
        draft_y_padding = button_side/2
        buttons = []
        x, y = draft_x_padding, screen_y/2-draft_y_padding-button_side
        for monster_name, monster_img in monsters[:6]:
            buttons.append(DraftButton(monster_name, (x,y), self.draft_button_size, ChooseDraft(monster_name), self.font, monster_img))
            x+=button_side+draft_x_padding
        x, y = draft_x_padding, screen_y/2+draft_y_padding
        for monster_name, monster_img in monsters[6:]:
            buttons.append(DraftButton(monster_name, (x,y), self.draft_button_size, ChooseDraft(monster_name), self.font, monster_img))
            x+=button_side+draft_x_padding
        return buttons
    
    def create_choose_team_limit_buttons(self):
        n = 1
        buttons = []
        spacing_x = self.main_menu_button_size[0]/2.5
        spacing_y = self.main_menu_button_size[1]/2
        
        y = screen_y/2-self.main_menu_button_size[1]*1.5-spacing_y
        for _ in range(3):
            x = screen_x/2-self.main_menu_button_size[0]-spacing_x
            for _ in range(2):
                buttons.append(self.create_menu_button(str(n), x, y, SetTeamLimitAction(n)))
                x+=self.main_menu_button_size[0]+spacing_x*2
                n+=1
            y+=self.main_menu_button_size[1]+spacing_y
        
        return buttons

    def create_change_monster_buttons(self, monsters, force_change = False):
        change_monster_buttons = []
        monsters = monsters.copy()
        if game.selected_monster.alive:
            monsters.remove(game.selected_monster) # escludo il mostro selezionato
        # qui calcolo le posizioni e dimensioni dei tasti in base al numero di mostri

        n = len(monsters)
        if not force_change:
            n+=1
        min_button_width = screen_x/5
        button_h = bar_h/2
        
        if n==1: # c'è solo un tasto
            button_w = min(screen_x, min_button_width)
            x, y = (screen_x - button_w) / 2, screen_y-bar_h + button_h / 2
            if not force_change:
                return [Button('Indietro', (x, y), (button_w, button_h), Back_to_choose_action(), self.font, self.inactive_main_menu_color, self.active_main_menu_color)]
            else:
                monster=monsters[0]
                return [Button(monster.name, (x, y), (button_w, button_h), ChooseMonster(monster), self.font, self.inactive_main_menu_color, self.active_main_menu_color)]

        extra_space = screen_x - n * min_button_width
        ideal_spacing = extra_space / (n - 1)
        min_spacing = screen_y/80
        max_spacing = screen_y/20
        spacing = max(min_spacing, min(ideal_spacing, max_spacing))
        buttons_size = ((screen_x - (n+1)*spacing)/n, button_h)
        x, y = spacing, screen_y-bar_h+buttons_size[1]/2
        if not force_change:
            back_button = Button('Indietro', (x, y), buttons_size, Back_to_choose_action(), self.font, self.inactive_main_menu_color, self.active_main_menu_color)
            change_monster_buttons.append(back_button)
            x += spacing+buttons_size[0]
        for monster in monsters:
            bt = Button(monster.name, (x, y), buttons_size, ChooseMonster(monster), self.font, self.inactive_main_menu_color, self.active_main_menu_color)
            change_monster_buttons.append(bt)
            x += spacing+buttons_size[0]
        return change_monster_buttons

class Button(pygame.sprite.Sprite):
    def __init__(self, name, pos, size, action, font, inactive_color, active_color):
        super().__init__()
        self.name = name
        self.pos = pos
        self.size = size
        self.action = action
        self.font = font
        self.active = False
        self.activable = True
        self.inactive_color = inactive_color
        self.active_color = active_color

        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect(topleft=self.pos)
        if self.font:
            text_size = self.rect.h//3
            text_font = pygame.font.Font(self.font, text_size)
            self.text_surface = text_font.render(self.name, True, (0, 0, 0))
            self.text_x = (self.rect.w - self.text_surface.get_width())/2
            self.text_y = (self.rect.h - self.text_surface.get_height())/2
        self.render()

    def render(self):
        color = self.active_color if self.active else self.inactive_color
        self.image.fill(color)
        self.image.blit(self.text_surface, (self.text_x,self.text_y))

    def set_active(self, value):
        self.active = value
        self.render()

    def activate(self):
        self.set_active(False)
        self.action.execute()

class DraftButton(Button):
    def __init__(self, name, pos, size, action, font, monster_image):
        self.base_img = pygame.transform.scale(monster_image, size)
        self.unselected_image = None
        super().__init__(name, pos, size, action, font, inactive_color=None, active_color=None)

        # creazione immagini selezionate e non
        self.w = self.size[0]
        self.selection_offset = self.w*0.05
        self.unselected_image = pygame.Surface((self.w+self.selection_offset*2, self.w+self.selection_offset*2))
        self.unselected_image.blit(self.base_img, (self.selection_offset,self.selection_offset))
        self.image = self.unselected_image

        self.rect = self.image.get_rect(topleft=self.pos)

        self.selected_image = pygame.Surface((self.w+self.selection_offset*2, self.w+self.selection_offset*2))
        selection_color = 'Yellow'
        selection_width = 2
        pygame.draw.rect(self.selected_image, selection_color, (0,0,self.w+self.selection_offset*2,self.w+self.selection_offset*2), selection_width)
        self.selected_image.blit(self.base_img, (self.selection_offset,self.selection_offset))

    def render(self):
        if self.active:
            self.image = self.selected_image
        else:
            self.image = self.unselected_image

    def activate(self):
        self.set_active(False)
        self.activable = False

        self.base_img = self.grayscale(self.base_img)
        self.unselected_image.blit(self.base_img, (self.selection_offset,self.selection_offset))
        self.selected_image.blit(self.base_img, (self.selection_offset,self.selection_offset))

        text_size = self.rect.h//2
        text_font = pygame.font.Font(self.font, text_size)
        player_text_surface = text_font.render(str(game.turn+1), True, game.team_colors[game.turn])
        text_x = (self.rect.w - player_text_surface.get_width())/2
        text_y = (self.rect.h - player_text_surface.get_height())/2
        self.selected_image.blit(player_text_surface, (text_x, text_y))
        self.unselected_image.blit(player_text_surface, (text_x, text_y))

        self.image = self.unselected_image

        self.action.execute()

    def grayscale(self, img): # scopiazzato 
        arr = pygame.surfarray.array3d(img).astype(float32)

        # luminosity method (vectorized)
        gray = (
            0.298 * arr[:, :, 0] +
            0.587 * arr[:, :, 1] +
            0.114 * arr[:, :, 2]
        )

        # ricrea RGB
        gray_arr = stack((gray, gray, gray), axis=-1)

        return pygame.surfarray.make_surface(gray_arr.astype(uint8))

main_menu_buttons_dim = (screen_x/4, screen_y/6)
moves_buttons_dim = (screen_x/6,screen_y/11)
draft_buttons_dim = (screen_x/9, screen_x/9)

button_factory = ButtonFactory(screen_size, main_menu_buttons_dim, moves_buttons_dim, draft_buttons_dim, game_font)

butt_startgame = button_factory.create_menu_button("Gioca", (screen_x - main_menu_buttons_dim[0]) / 2, screen_y/2 - main_menu_buttons_dim[1]*1.5, PlayAction())
butt_exitgame = button_factory.create_menu_button("Esci", (screen_x - main_menu_buttons_dim[0]) / 2, screen_y/2 + main_menu_buttons_dim[1]*0.5, ExitAction(game))

game.refresh_buttons([butt_startgame, butt_exitgame])

bar_buttons_y = screen_y - bar_h/2 - main_menu_buttons_dim[1]/2
butt_fight = button_factory.create_menu_button("Combatti", screen_x/4 - main_menu_buttons_dim[0]/2, bar_buttons_y, ChooseMove())
butt_changemonster = button_factory.create_menu_button("Cambia", screen_x*3/4 - main_menu_buttons_dim[0]/2, bar_buttons_y, ChangeMonster())


class MenuLayouts:
    def __init__(self):
        self.layouts = {
            "start": {
                "buttons": [butt_startgame, butt_exitgame],
                "rows": 2,
                "cols": 1
            },
            "choose_action": {
                "buttons": [butt_fight, butt_changemonster],
                "rows": 1,
                "cols": 2
            },
            "choose_move": {
                "buttons": None,
                "rows": 2,
                "cols": 3
            },
            "draft": {
                "buttons": None,
                "rows": 2,
                "cols": 6
            },
            "choose_team_limit": {
                "buttons": None,
                "rows": 3,
                "cols": 2
            },
            "change_monster": {
                "buttons": None,
                "rows": 1,
                "cols": game.team_limit
            }
        }

    def update_menu_buttons(self, menu_name, new_buttons):
        self[menu_name]['buttons'] = new_buttons
    
    def update_change_monster_buttons(self, force_change=False):
        new_buttons = button_factory.create_change_monster_buttons(game.teams[game.selected_monster.team], force_change=force_change)
        self['change_monster']['cols'] = len(new_buttons)
        self.update_menu_buttons('change_monster', new_buttons)

    def update_moves_buttons(self):
        new_moves = button_factory.create_move_buttons(game.selected_monster.moves)
        self.update_menu_buttons('choose_move', new_moves)

    def __getitem__(self, key): # per comodità
        return self.layouts[key]

MENU_LAYOUTS = MenuLayouts()

def buttons_check_input(event):
    layout = MENU_LAYOUTS[game.active_menu]
    buttons = layout['buttons']
    rows = layout['rows']
    cols = layout['cols']

    # posizione del bottone selezionato (riga e colonna):
    i = game.selected_button_i
    r = i // cols
    c = i % cols

    if event.key == pygame.K_RETURN:
        if buttons[i].activable:
            buttons[i].activate()
        return

    elif event.key == pygame.K_RIGHT:
        c = (c + 1) % cols
    elif event.key == pygame.K_LEFT:
        c = (c - 1) % cols
    elif event.key == pygame.K_DOWN:
        r = (r + 1) % rows
    elif event.key == pygame.K_UP:
        r = (r - 1) % rows
    else:
        return

    new_i = r * cols + c
    buttons[i].set_active(False)
    game.selected_button_i = new_i
    buttons[new_i].set_active(True)