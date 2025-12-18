from pygame.sprite import Sprite
from game_assets import attacking_monster_pos, defending_monster_pos, screen_x, game

MONSTERS_STATES = {
    'attacking': attacking_monster_pos,
    'defending': defending_monster_pos
}

class VisualMonster(Sprite):
    def __init__(self, monster, start_pos, state):
        super().__init__()
        self.monster = monster
        self.pos = start_pos
        self.state=state
        self.front_image=monster.front_image
        self.back_image=monster.back_image
        self.image = self.back_image if self.state=='attacking' else self.front_image
        self.rect = self.image.get_rect(topleft=self.pos)

    def update(self, screen):
        if game.is_in_animation: # se sta facendo lo scambio turni, vede quando cambiare lo sprite
            if self.pos[0] < 0-self.rect.width:
                self.state='attacking'
            elif self.pos[0]> screen_x:
                self.state='defending'
            self.image = self.back_image if self.state=='attacking' else self.front_image
        
        screen.blit(self.image, self.pos)
        self.rect.topleft = self.pos
        if self.monster.hp<=0:
            #self.kill()
            self.image.fill('Red')
