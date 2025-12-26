from pygame import Surface, font
from pygame.sprite import Sprite, GroupSingle
from game_assets import screen_x, screen_y, bar_h, monster_size, attacking_monster_pos, defending_monster_pos, game_font
font.init()
# semplicemente il rettangolo in basso con le mosse ecc.

class MatchBar(Sprite):
    def __init__(self):
        super().__init__()
        self.state = None
        size = (screen_x, bar_h)
        self.image = Surface(size)
        self.image.fill("#FFFFFF")
        self.pos = (0, screen_y-bar_h)
        self.rect = self.image.get_rect(topleft = self.pos)

bar = GroupSingle(MatchBar())

class StatsBox(Sprite):
    def __init__(self, pos):
        super().__init__()
        self.monster = None
        size_x, size_y = (monster_size[0], monster_size[1]/4)
        self.image = Surface((size_x, size_y))
        self.image.fill("#FFFFFF")
        self.pos = pos
        self.rect = self.image.get_rect(topleft = self.pos)

        self.bars_size_x = size_x*29/30
        self.hp_bar_size_y = size_y/5
        self.xp_bar_size_y = size_y/10

        self.spacing = (size_x - self.bars_size_x)/2
        self.bars_x = size_x-self.bars_size_x-self.spacing
        self.hp_bar_y = self.spacing
        self.xp_bar_y = self.hp_bar_y+self.hp_bar_size_y

        self.hp_bar = Surface((self.bars_size_x, self.hp_bar_size_y))
        self.hp_bar_pos = (self.bars_x, self.hp_bar_y)

        self.xp_bar = Surface((self.bars_size_x, self.xp_bar_size_y))
        self.xp_bar.fill("#7AA5EF")
        self.xp_bar_pos = (self.bars_x, self.xp_bar_y)

        text_size = round((size_y-self.xp_bar_y)/2)
        self.text_font = font.Font(game_font, text_size)
        self.text_pos = (self.spacing,self.xp_bar_y+self.xp_bar_size_y+self.spacing)

        hp_text_size = round(self.hp_bar_size_y)-2
        self.hp_text_font = font.Font(game_font, hp_text_size)
        self.hp_text_pos = (self.spacing,1)
    
    def set_monster(self, monster):
        self.monster = monster

    def update(self):
        self.image.fill('#FFFFFF')

        # hp bar
        hp_ratio = self.monster.hp/self.monster.max_hp
        self.hp_bar.fill("#FC2C2C")
        green_portion = self.bars_size_x*hp_ratio
        if green_portion>0:
            green_hp = Surface((green_portion,self.hp_bar_size_y))
            green_hp.fill("#2CF150")
            self.hp_bar.blit(green_hp, (0,0))
        hp_text = str(self.monster.hp)+'/'+str(self.monster.max_hp)
        hp_text_surface = self.hp_text_font.render(hp_text, True, (0, 0, 0))
        self.hp_bar.blit(hp_text_surface, self.hp_text_pos)

        self.image.blit(self.hp_bar, self.hp_bar_pos)

        # xp bar
        self.image.blit(self.xp_bar, self.xp_bar_pos)

        #monster name
        monster_name = self.monster.name
        name_surface = self.text_font.render(monster_name, True, (0, 0, 0))
        self.image.blit(name_surface, self.text_pos)

attacking_monster_box_pos = (attacking_monster_pos[0]+monster_size[0]*1.2, attacking_monster_pos[1]+monster_size[1]*0.2)
attacking_monster_box = StatsBox(attacking_monster_box_pos)

defending_monster_box_pos = (defending_monster_pos[0]-monster_size[0]*0.2-attacking_monster_box.rect.w, defending_monster_pos[1]+monster_size[1]*0.2)
defending_monster_box = StatsBox(defending_monster_box_pos)