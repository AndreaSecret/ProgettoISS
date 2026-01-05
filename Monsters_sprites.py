from pygame.sprite import Sprite
from game_assets import screen_x

# class for graphic components of monsters

class VisualMonster(Sprite):
    def __init__(self, monster, start_pos, state, animation_manager):
        super().__init__()
        self.monster = monster
        self.pos = start_pos
        self.state=state
        self.front_image=monster.front_image
        self.back_image=monster.back_image
        self.update_image()
        self.rect = self.image.get_rect(topleft=self.pos)
        self.animation_manager = animation_manager
    
    def update_image(self):
        self.image = self.back_image if self.state=='attacking' else self.front_image

    def update(self, screen):
        if self.animation_manager.current == 'switching_sides': # se sta facendo lo scambio turni, vede quando cambiare lo sprite
            if self.pos[0] < 0-self.rect.width:
                self.state='attacking'
            elif self.pos[0]> screen_x:
                self.state='defending'
            self.update_image()
            self.rect.topleft = self.pos
        
        screen.blit(self.image, self.pos)

        if self.monster.check_death(): # controlla se il mostro è morto
            self.death_effect()
        
        return self.monster.alive

    def change_monster(self, monster):
        self.monster = monster
        self.front_image = monster.front_image
        self.back_image = monster.back_image
        self.image = self.back_image

    def death_effect(self):
        self.animation_manager.add_death_anim(self)
