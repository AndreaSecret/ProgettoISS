
# file per i tasti
import unittest
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
        game.buttons.empty()
        game.buttons.add(butt_fight, butt_changemonster)

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
        

# button factory
class ButtonFactory:
    def __init__(self, screen_size, button_size, font):
        self.screen_size = screen_size
        self.button_size = button_size
        self.font = font

    def create_button(self, text, x, y, action):
        return Button(text, (x, y), self.button_size, action, self.font)
    


class Button(pygame.sprite.Sprite):
    def __init__(self, name, pos, size, action, font):
        super().__init__()
        self.name = name
        self.pos = pos
        self.size = size
        self.action = action
        self.font = font
        self.active = False

        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect(topleft=self.pos)
        self.render()

    def render(self):
        color = "#FF8801" if self.active else "#FFFF01"
        self.image.fill(color)
        text_surface = self.font.render(self.name, True, (0, 0, 0))
        self.image.blit(text_surface, (0,0))

    def set_active(self, value):
        self.active = value
        self.render()

    def activate(self):
        self.action.execute()


buttons_dim = (400, 130)
button_factory = ButtonFactory(screen_size, buttons_dim, game_font)

butt_startgame = button_factory.create_button("Gioca", (screen_x - buttons_dim[0]) / 2, 200, PlayAction())
butt_exitgame = button_factory.create_button("Esci", (screen_x - buttons_dim[0]) / 2, 400, ExitAction(game))

buttons = [butt_startgame, butt_exitgame]
game.buttons = pygame.sprite.Group(buttons)

butt_fight = button_factory.create_button("Combatti", screen_x/4-buttons_dim[0]/2, 4/5* screen_y, ChooseMove())
butt_changemonster = button_factory.create_button("Cambia", screen_x*3/4-buttons_dim[0]/2, 4/5* screen_y, ChangeMonster())