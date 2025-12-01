
# main loop file

import pygame
from pygame.locals import FULLSCREEN
from game_assets import *
from buttons import buttons
from monsters import drago, serpe
from bar_menu import bar

pygame.init()
clock = pygame.time.Clock()
fps = 30
screen=pygame.display.set_mode(screen_size, FULLSCREEN)


buttons[game.selected_button_i].set_active(True)


def menu_check_input(buttons, event):
    if game.start_menu:
        if event.key == pygame.K_UP:
            buttons[game.selected_button_i].set_active(False) #ricoloro a normale il tasto
            game.selected_button_i = (game.selected_button_i-1) % len(buttons) #trovo il nuovo tasto da evidenziare
            buttons[game.selected_button_i].set_active(True) #e lo coloro
        if event.key == pygame.K_DOWN: #analogo a K_UP
            buttons[game.selected_button_i].set_active(False)
            game.selected_button_i = (game.selected_button_i+1) % len(buttons)
            buttons[game.selected_button_i].set_active(True)
        if event.key == pygame.K_RETURN: #il bottone si attiva cliccando il tasto enter
            buttons[game.selected_button_i].activate()

while game.run:
    key_input=pygame.key.get_pressed()
    screen.fill('Black')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.run = False
        if event.type == pygame.KEYDOWN:
            menu_check_input(buttons, event)
            if event.key == pygame.K_ESCAPE:
                game.run = False
            
    if game.game_start:
        screen.blit(drago.image, (screen_x/2-screen_x/4,screen_y/4))
        screen.blit(serpe.image, (screen_x/2+screen_x/4-serpe.image.get_size()[0],screen_y/4))
        screen.blit(bar, (0, 3/4*screen_y))
    game.buttons.draw(screen)
    pygame.display.update()
    clock.tick(fps)