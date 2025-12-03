
# main loop file

import pygame
from pygame.locals import FULLSCREEN
from game_assets import *
from monsters import drago, serpe
from bar_menu import bar
from buttons import buttons_check_input

pygame.init()
clock = pygame.time.Clock()
fps = 30
screen=pygame.display.set_mode(screen_size, FULLSCREEN)


while game.run:
    key_input=pygame.key.get_pressed()
    screen.fill('Black')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.run = False
        if event.type == pygame.KEYDOWN:
            buttons_check_input(event)
            if event.key == pygame.K_ESCAPE:
                game.run = False
            
    if game.game_start:
        screen.blit(drago.image, (screen_x/2-screen_x/4,screen_y/4))
        screen.blit(serpe.image, (screen_x/2+screen_x/4-serpe.image.get_size()[0],screen_y/4))
        screen.blit(bar, (0, 3/4*screen_y))
    game.buttons_group.draw(screen)
    pygame.display.update()
    clock.tick(fps)