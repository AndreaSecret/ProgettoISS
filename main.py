# main loop file
import pygame
from pygame.locals import FULLSCREEN
from game_assets import game, screen_size
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
            if not game.is_in_animation: #se c'è un animazione blocco gli input
                buttons_check_input(event)
            if event.key == pygame.K_ESCAPE:
                game.run = False
            
    if game.game_start:
        game.update(screen)

    game.buttons_group.draw(screen)
    pygame.display.update()
    clock.tick(fps)