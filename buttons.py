
# file per i tasti
from abc import ABC, abstractmethod
import pygame
from game_assets import *


#button action functions
class ButtonAction(ABC):
    @abstractmethod
    def execute(self):
        pass

class PlayAction(ButtonAction):
    def execute(self):
        game.start_menu = False
        game.game_start = True
        game.start_menu = False
        game.choose_action_menu = True
        game.refresh_buttons([butt_fight, butt_changemonster])
        

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
        game.choose_move_menu = True
        game.choose_action_menu = False
        game.refresh_buttons([mossa1, mossa3])

class UseMove(ButtonAction):
    def __init__(self, move):
        self.move = move
    def execute(self):
        self.move.execute()
        

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
    def create_move_button(self, text, x, y, action):
        return Button(text, (x, y), self.moves_button_size, action, self.font, self.inactive_move_color, self.active_move_color)
    


class Button(pygame.sprite.Sprite):
    def __init__(self, name, pos, size, action, font, inactive_color, active_color):
        super().__init__()
        self.name = name
        self.pos = pos
        self.size = size
        self.action = action
        self.font = font
        self.active = False
        self.inactive_color = "#FFFF01"
        self.active_color = "#FF8801"

        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect(topleft=self.pos)
        self.render()

    def render(self):
        color = self.active_color if self.active else self.inactive_color
        self.image.fill(color)
        text_surface = self.font.render(self.name, True, (0, 0, 0))
        self.image.blit(text_surface, (0,0))

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

moves_padding = screen_y/40
mossa1 = button_factory.create_move_button("mossa1", moves_padding, 3/4* screen_y+moves_padding, ChangeMonster())
mossa3 = button_factory.create_move_button("mossa1", moves_padding, 3/4* screen_y+moves_padding*2+moves_buttons_dim[1], ChangeMonster())





def buttons_check_input(event):
    if game.start_menu:
        if event.key == pygame.K_UP:
            game.buttons[game.selected_button_i].set_active(False) #ricoloro a normale il tasto
            game.selected_button_i = (game.selected_button_i-1) % len(game.buttons) #trovo il nuovo tasto da evidenziare
            game.buttons[game.selected_button_i].set_active(True) #e lo coloro
        if event.key == pygame.K_DOWN: #analogo a K_UP
            game.buttons[game.selected_button_i].set_active(False)
            game.selected_button_i = (game.selected_button_i+1) % len(game.buttons)
            game.buttons[game.selected_button_i].set_active(True)
        if event.key == pygame.K_RETURN: #il bottone si attiva cliccando il tasto enter
            game.buttons[game.selected_button_i].activate()
    elif game.choose_action_menu:
        if event.key == pygame.K_RIGHT:
            game.buttons[game.selected_button_i].set_active(False)
            game.selected_button_i = (game.selected_button_i-1) % len(game.buttons) 
            game.buttons[game.selected_button_i].set_active(True) 
        if event.key == pygame.K_LEFT:
            game.buttons[game.selected_button_i].set_active(False)
            game.selected_button_i = (game.selected_button_i+1) % len(game.buttons)
            game.buttons[game.selected_button_i].set_active(True)
        if event.key == pygame.K_RETURN:
            game.buttons[game.selected_button_i].activate()