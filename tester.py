moves = {
    1: '1',
    2: None,
    3: '3'
}

print([moves[base] or base for base in moves])

# import pygame
# from buttons import DraftButton, ChangeMonster
# drago_front_img =  pygame.transform.scale(pygame.image.load('monster_sprites/Drago/drago_front.png'), (150,150))
# pygame.init()
# clock = pygame.time.Clock()
# fps = 30
# screen=pygame.display.set_mode((1000,600))

# bt = DraftButton((100,100), (150,150), ChangeMonster, drago_front_img)


# run = True
# while run:
#     key_input=pygame.key.get_pressed()
#     screen.fill('Black')
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_RIGHT:
#                 bt.set_active(True)
#             if event.key == pygame.K_LEFT:
#                 bt.set_active(False)
#     screen.blit(bt.image, bt.pos)
#     pygame.display.update()
#     clock.tick(fps)