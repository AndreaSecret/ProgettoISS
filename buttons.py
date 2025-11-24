
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
        print("Il gioco non esiste...")

class ExitAction(ButtonAction):
    def __init__(self, game):
        self.game = game

    def execute(self):
        self.game.run = False

# button factory
class ButtonFactory:
    def __init__(self, screen_size, button_size, font):
        self.screen_size = screen_size
        self.button_size = button_size
        self.font = font

    def create_button(self, text, y, action):
        x = (self.screen_size[0] - self.button_size[0]) / 2
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

buttons_dim = (250, 90)
button_factory = ButtonFactory(screen_size, buttons_dim, game_font)

butt1 = button_factory.create_button("Gioca", 200, PlayAction())
butt2 = button_factory.create_button("Esci", 400, ExitAction(game))

buttons = [butt1, butt2]
buttons_group = pygame.sprite.Group(buttons)