import pygame, sys
pygame.init()
game_font = pygame.font.Font('game_files/PixeloidSans.ttf', 70)
text_surface = game_font.render('Ciaooooo', True, (0,0,0))
clock = pygame.time.Clock()
fps = 30
screen=pygame.display.set_mode((1000, 600))
run = True
while run:
    key_input=pygame.key.get_pressed()
    screen.fill('White')
    screen.blit(text_surface, (100,100))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                run = False
                print('hshdgh')
    pygame.display.update()
    clock.tick(fps)