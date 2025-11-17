import pygame
import sys

pygame.init()
clock = pygame.time.Clock()
fps = 30
screen_size = (1000, 600)
screen=pygame.display.set_mode(screen_size)

font = pygame.font.SysFont('Comic Sans MS', 30)

class Tasto(pygame.sprite.Sprite):
    def __init__(self, name, pos, size, func):
        super().__init__()
        self.name = name
        self.pos = pos
        self.size = size
        self.activate = func
        self.image = pygame.Surface(self.size)
        self.set_color("#FFFF01")
        self.rect = self.image.get_rect(topleft = self.pos)
    def set_color(self, color):
        self.image.fill(color)
        text_surface = font.render(self.name, True, (0, 0, 0))
        self.image.blit(text_surface, (0,0)) #da cambiare la posizione della scritta probably

def func1():
    print('Il gioco non esiste...')
def exit_game():
    game.run = False

dim_tasti = (250, 90)
tasto1 = Tasto('Gioca', ((screen_size[0]-dim_tasti[0])/2, 200), dim_tasti, func1)
tasto2 = Tasto('Esci', ((screen_size[0]-dim_tasti[0])/2, 400), dim_tasti, exit_game)
tasti_list = [tasto1, tasto2]
tasti = pygame.sprite.Group(tasti_list)



class Game:
    def __init__(self):
        self.run = True
game = Game()

selected_button_i = 0
selected_button = tasti_list[0]
selected_button.set_color("#FF8801")

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
                selected_button.set_color("#FFFF01") #ricoloro a normale il tasto
                selected_button_i = (selected_button_i-1) % len(tasti_list) #trovo il nuovo tasto da evidenziare
                selected_button = tasti_list[selected_button_i] 
                selected_button.set_color("#FF8801") #e lo coloro
            if event.key == pygame.K_DOWN: #analogo a K_UP
                selected_button.set_color("#FFFF01")
                selected_button_i = (selected_button_i+1) % len(tasti_list)
                selected_button = tasti_list[selected_button_i]
                selected_button.set_color("#FF8801")
            if event.key == pygame.K_RETURN: #il bottone si attiva cliccando il tasto enter
                selected_button.activate()
            
    tasti.draw(screen)
    pygame.display.update()
    clock.tick(fps)