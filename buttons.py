# file per i tasti
from abc import ABC, abstractmethod
import pygame
from game_assets import *
from monsters import drago, serpe
from Monsters_sprites import VisualMonster
from animations import switch_animation


#button action functions
class ButtonAction(ABC):
    @abstractmethod
    def execute(self):
        pass

class PlayAction(ButtonAction):
    def execute(self):
        global MENU_LAYOUTS
        game.start_game(serpe, drago, VisualMonster)
        mosse=button_factory.create_move_buttons(game.selected_monster.moves)
        MENU_LAYOUTS['choose_move']['buttons'] = mosse
        MENU_LAYOUTS[game.active_menu]['buttons'][game.selected_button_i].set_active(False)
        game.active_menu = 'choose_action'
        game.refresh_buttons(MENU_LAYOUTS['choose_action']['buttons'])
        

class ExitAction(ButtonAction):
    def __init__(self, game):
        self.game = game

    def execute(self):
        self.game.run = False

class ChangeMonster(ButtonAction):
    def execute(self):
        print('hai solo un mostro')

class ChooseMove(ButtonAction):
    def execute(self):
        MENU_LAYOUTS[game.active_menu]['buttons'][game.selected_button_i].set_active(False)
        game.active_menu = 'choose_move'
        game.refresh_buttons(MENU_LAYOUTS['choose_move']['buttons'])

class UseMove(ButtonAction):
    def __init__(self, move):
        self.move = move
    def execute(self):
        self.move.execute(game.selected_monster, game.enemy_monster)

        
        global MENU_LAYOUTS
        MENU_LAYOUTS[game.active_menu]['buttons'][game.selected_button_i].set_active(False)
        switch_anims = switch_animation(game.selected_monster_sprite, game.enemy_monster_sprite)
        game.add_animation(switch_anims)
        new_moves = game.switch_turn()
        mosse=button_factory.create_move_buttons(new_moves)
        MENU_LAYOUTS['choose_move']['buttons'] = mosse
        game.refresh_buttons(MENU_LAYOUTS['choose_action']['buttons'])

        

# button factory
class ButtonFactory:
    def __init__(self, screen_size, main_menu_button_size, moves_button_size, font):
        self.screen_size = screen_size
        self.main_menu_button_size = main_menu_button_size
        self.moves_button_size = moves_button_size
        self.font = font
        self.inactive_main_menu_color = "#FFFF01"
        self.active_main_menu_color = "#FF8801"
        self.inactive_move_color = "#BFE6EA"
        self.active_move_color = "#358FC7"

    def create_menu_button(self, text, x, y, action):
        return Button(text, (x, y), self.main_menu_button_size, action, self.font, self.inactive_main_menu_color, self.active_main_menu_color)
    def create_move_buttons(self, moves: list):
        moves_padding = screen_y/40
        # posizioni dei 4 bottoni delle mosse:
        x1,y1 = moves_padding, 3/4* screen_y+moves_padding
        x2,y2 = moves_padding*2+self.moves_button_size[0], 3/4* screen_y+moves_padding
        x3,y3 = moves_padding, 3/4* screen_y+moves_padding*2+self.moves_button_size[1]
        x4,y4 = moves_padding*2+self.moves_button_size[0], 3/4* screen_y+moves_padding*2+self.moves_button_size[1]

        mossa1 = Button(moves[0].name, (x1, y1), self.moves_button_size, UseMove(moves[0]), self.font, self.inactive_move_color, self.active_move_color)
        mossa2 = Button(moves[1].name, (x2, y2), self.moves_button_size, UseMove(moves[1]), self.font, self.inactive_move_color, self.active_move_color)
        mossa3 = Button(moves[2].name, (x3, y3), self.moves_button_size, UseMove(moves[2]), self.font, self.inactive_move_color, self.active_move_color)
        mossa4 = Button(moves[3].name, (x4, y4), self.moves_button_size, UseMove(moves[3]), self.font, self.inactive_move_color, self.active_move_color)

        return [mossa1,mossa2,mossa3,mossa4]


class Button(pygame.sprite.Sprite):
    def __init__(self, name, pos, size, action, font, inactive_color, active_color):
        super().__init__()
        self.name = name
        self.pos = pos
        self.size = size
        self.action = action
        self.font = font
        self.active = False
        self.inactive_color = inactive_color
        self.active_color = active_color

        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect(topleft=self.pos)

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
        self.action.execute()


main_menu_buttons_dim = (screen_x/4, screen_y/6)
moves_buttons_dim = (screen_x/6,screen_y/11)
button_factory = ButtonFactory(screen_size, main_menu_buttons_dim, moves_buttons_dim, game_font)

butt_startgame = button_factory.create_menu_button("Gioca", (screen_x - main_menu_buttons_dim[0]) / 2, screen_y/2 - main_menu_buttons_dim[1]*1.5, PlayAction())
butt_exitgame = button_factory.create_menu_button("Esci", (screen_x - main_menu_buttons_dim[0]) / 2, screen_y/2 + main_menu_buttons_dim[1]*0.5, ExitAction(game))

game.refresh_buttons([butt_startgame, butt_exitgame])

butt_fight = button_factory.create_menu_button("Combatti", screen_x/4 - main_menu_buttons_dim[0]/2, 4/5* screen_y, ChooseMove())
butt_changemonster = button_factory.create_menu_button("Cambia", screen_x*3/4 - main_menu_buttons_dim[0]/2, 4/5* screen_y, ChangeMonster())


MENU_LAYOUTS = {
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
        "cols": 2
    }
}

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