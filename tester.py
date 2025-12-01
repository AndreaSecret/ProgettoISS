import pygame, sys
pygame.init()

clock = pygame.time.Clock()
fps = 30
screen=pygame.display.set_mode((1000, 600))

run = True
while run:
    key_input=pygame.key.get_pressed()
    screen.fill('Black')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
                print('hshdgh')