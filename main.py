
# main loop file

import pygame
import sys
from game_assets import *
from buttons import buttons, buttons_group

pygame.init()
clock = pygame.time.Clock()
fps = 30
screen=pygame.display.set_mode(screen_size)


selected_button_i = 0
buttons[selected_button_i].set_active(True)

while game.run:
    key_input=pygame.key.get_pressed()
    screen.fill('Black')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            game.run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                buttons[selected_button_i].set_active(False) #ricoloro a normale il tasto
                selected_button_i = (selected_button_i-1) % len(buttons) #trovo il nuovo tasto da evidenziare
                buttons[selected_button_i].set_active(True) #e lo coloro
            if event.key == pygame.K_DOWN: #analogo a K_UP
                buttons[selected_button_i].set_active(False)
                selected_button_i = (selected_button_i+1) % len(buttons)
                buttons[selected_button_i].set_active(True)
            if event.key == pygame.K_RETURN: #il bottone si attiva cliccando il tasto enter
                buttons[selected_button_i].activate()
            
    buttons_group.draw(screen)
    pygame.display.update()
    clock.tick(fps)