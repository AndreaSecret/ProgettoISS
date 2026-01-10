# main loop file
import pygame
from pygame.locals import FULLSCREEN
from game_assets import game, screen_size
from buttons import buttons_check_input

pygame.init()
clock = pygame.time.Clock()
fps = 30
screen=pygame.display.set_mode(screen_size, FULLSCREEN)
background = pygame.transform.scale(pygame.image.load('battle_bg.jpeg').convert(), screen_size) #fatta da noi 
while game.run:
    screen.fill('Black')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.run = False
        if event.type == pygame.KEYDOWN:
            if not game.is_in_animation: #se c'è un animazione blocco gli input
                buttons_check_input(event)
            if event.key == pygame.K_ESCAPE:
                game.run = False
            
    game.update(screen, background=background)

    game.buttons_group.draw(screen)
    pygame.display.update()
    clock.tick(fps)